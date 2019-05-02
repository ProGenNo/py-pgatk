"""
This module implements en Ensembl data grabber for a given Ensembl Service instance.

Some of the use cases for this module:
    1. Given a species ID, download its protein sequence data, with the option of decompressing it or not.
    2. Given a species ID, collect its GTF data, with the option of decompressing it or not.
"""

import os

# App imports
from json import loads
from requests import get
from toolbox.general import ParameterConfiguration, check_create_folders, download_file


class EnsemblDataDownloadService(ParameterConfiguration):
    """
    This Service is in charge of grabbing data (download) from Ensembl to a local repository
    """

    CONFIG_KEY_DATA_DOWNLOADER = 'ensembl_data_downloader'
    CONFIG_OUTPUT_DIRECTORY = 'output_directory'
    CONFIG_KEY_ENSEMBL_FTP = 'ensembl_ftp'
    CONFIG_ENSEMBL_API = 'ensembl_api'
    CONFIG_ENSEMBL_API_SERVER = 'server'
    CONFIG_ENSEMBL_API_SPECIES = 'species'
    CONFIG_KEY_BASE_URL = 'base_url'
    CONFIG_KEY_FOLDER_PREFIX_RELEASE = 'folder_prefix_release'
    CONFIG_KEY_FOLDER_NAME_FASTA = 'folder_name_fasta'
    CONFIG_KEY_FOLDER_NAME_PROTEIN_SEQUENCES = 'folder_name_protein_sequences'
    CONFIG_KEY_FOLDER_NAME_GTF = 'folder_name_gtf'
    CONFIG_KEY_REWRITE_LOCAL_PATH_ENSEMBL_REPO = 'rewrite_local_path_ensembl_repo'
    CONFIG_KEY_ENSEMBL_FILE_NAMES = 'ensembl_file_names'
    CONFIG_KEY_PROTEIN_SEQUENCE_FILE = 'protein_sequence_file'
    CONFIG_KEY_FILE_TYPE = 'file_type'
    CONFIG_KEY_FILE_SUFFIXES = 'file_suffixes'
    CONFIG_KEY_FILE_EXTENSION = 'file_extension'
    CONFIG_KEY_GTF_FILE = 'gtf_file'
    CONFIG_REST_API_TAXON_ID = 'taxon_id'
    CONFIG_TAXONOMY = 'taxonomy'
    CONFIG_KEY_SKIP_PROTEIN = 'skip_protein'
    CONFIG_KEY_SKIP_GTF = 'skip_gtf'
    CONFIG_KEY_SKIP_CDS = 'skip_cds'
    CONFIG_KEY_SKIP_NCRNA = 'skip_ncrna'

    def __init__(self, config_file, pipeline_arguments):
        """
        Init the class with the specific parameters.
        :param config_file configuration file
        :param pipeline_arguments pipelines arguments
        """
        super(EnsemblDataDownloadService, self).__init__(self.CONFIG_KEY_DATA_DOWNLOADER, config_file,
                                                         pipeline_arguments)

        self._ensembl_species = []
        if self.CONFIG_OUTPUT_DIRECTORY in self.get_pipeline_parameters():
            self._local_path_ensembl = self.get_pipeline_parameters()[self.CONFIG_OUTPUT_DIRECTORY]
        else:
            self._local_path_ensembl = self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][
                self.CONFIG_OUTPUT_DIRECTORY]

        self.prepare_local_ensembl_repository()

    def get_local_path_root_ensembl_repo(self):
        return self._local_path_ensembl

    def prepare_local_ensembl_repository(self):
        self.get_logger().debug(
            "Preparing local Ensembl repository, root folder - '{}'".format(self.get_local_path_root_ensembl_repo()))
        check_create_folders([self.get_local_path_root_ensembl_repo()])
        self.get_logger().debug(
            "Local path for Ensembl Release - '{}'".format(self.get_local_path_root_ensembl_repo()))

    def get_species_from_rest(self):
        """
        Get the list of species from ENSEMBL rest API.
        :return:
        """
        server = self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][self.CONFIG_ENSEMBL_API][
            self.CONFIG_ENSEMBL_API_SERVER]
        endpoint = self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][self.CONFIG_ENSEMBL_API][
            self.CONFIG_ENSEMBL_API_SPECIES]
        species_info = loads(get(server + endpoint, headers={"Content-Type": 'application/json'}).text)
        self._ensembl_species = species_info['species']
        return self._ensembl_species

    def download_database_by_species(self):
        """
        This method takes a list of Taxonomies from the commandline parameters and download the Protein fasta files
        and the gtf files.
        :return:
        """
        self.get_species_from_rest()
        species_parameters = self.get_pipeline_parameters()[self.CONFIG_TAXONOMY]
        species_list = species_parameters.split(",")
        total_files = []
        if species_list is None or len(species_list) == 0 or len(species_parameters) == 0:
            for species in self._ensembl_species:
                self.get_logger().debug(
                    "Downloading the data for the specie -- " + species[self.CONFIG_REST_API_TAXON_ID])
                if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_PROTEIN]:
                    files = self.get_pep_files(species)
                if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_GTF]:
                    gtf_files = self.get_gtf_files(species)
                    files.extend(gtf_files)
                if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_CDS]:
                    cds_files = self.get_cds_files(species)
                    files.extend(cds_files)
                if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_NCRNA]:
                    ncrna_files = self.get_ncrna_files(species)
                    files.extend(ncrna_files)
                total_files.extend(files)
                self.get_logger().debug("Files downloaded -- " + ",".join(files))
                total_files.extend(files)
        else:
            for species_id in species_list:
                for species in self._ensembl_species:
                    if species_id == species[self.CONFIG_REST_API_TAXON_ID]:
                        self.get_logger().debug(
                            "Downloading the data for the specie -- " + species[self.CONFIG_REST_API_TAXON_ID])
                        if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_PROTEIN]:
                            files = self.get_pep_files(species)
                        if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_GTF]:
                            gtf_files = self.get_gtf_files(species)
                            files.extend(gtf_files)
                        if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_CDS]:
                            cds_files = self.get_cds_files(species)
                            files.extend(cds_files)
                        if not self.get_pipeline_parameters()[self.CONFIG_KEY_SKIP_NCRNA]:
                            ncrna_files = self.get_ncrna_files(species)
                            files.extend(ncrna_files)
                        total_files.extend(files)
                        self.get_logger().debug("Files downloaded -- " + ",".join(files))
                        total_files.extend(files)

        return total_files

    def get_cds_files(self, species: dict) -> list:
        """
        Get the cds files for an specific species object.
        :return: List of files names.
        """
        files = []
        try:
            file_name = '{}.{}.cds.all.fa.gz'.format(species['name'][0].upper() + species['name'][1:],
                                                     species['assembly'])
            file_url = '{}/release-{}/fasta/{}/cds/{}'.format(
                self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][self.CONFIG_KEY_ENSEMBL_FTP][
                    self.CONFIG_KEY_BASE_URL],
                species['release'], species['name'], file_name)
            files.append(download_file(file_url, self.get_local_path_root_ensembl_repo() + '/' + file_name))
        except KeyError:
            print("No valid info is available species: ", species)

        return files

    def get_ncrna_files(self, species: dict) -> list:
        """
        Get the cds files for an specific species object.
        :return: List of files names.
        """
        files = []
        try:
            file_name = '{}.{}.ncrna.fa.gz'.format(species['name'][0].upper() + species['name'][1:],
                                                     species['assembly'])
            file_url = '{}/release-{}/fasta/{}/ncrna/{}'.format(
                self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][self.CONFIG_KEY_ENSEMBL_FTP][
                    self.CONFIG_KEY_BASE_URL],
                species['release'], species['name'], file_name)
            files.append(download_file(file_url, self.get_local_path_root_ensembl_repo() + '/' + file_name))
        except KeyError:
            print("No valid info is available species: ", species)

        return files

    def get_pep_files(self, species: dict) -> list:
        """
        Get the peptide files for an specific species object.
        :return: List of files names.
        """
        files = []
        try:
            file_name = '{}.{}.pep.all.fa.gz'.format(species['name'][0].upper() + species['name'][1:],
                                                     species['assembly'])
            file_url = '{}/release-{}/fasta/{}/pep/{}'.format(
                self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][self.CONFIG_KEY_ENSEMBL_FTP][
                    self.CONFIG_KEY_BASE_URL],
                species['release'], species['name'], file_name)
            files.append(download_file(file_url, self.get_local_path_root_ensembl_repo() + '/' + file_name))
        except KeyError:
            print("No valid info is available species: ", species)

        return files

    def get_gtf_files(self, species: dict) -> list:
        """
        This method retrieve the gtf files for an specific specie object
        :param species:
        :return:
        """
        """
          Generate GTF file name from the species info and download the GTF file
          """
        files = []
        try:
            file_name = '{}.{}.{}.gtf.gz'.format(species['name'][0].upper() + species['name'][1:], species['assembly'],
                                                 species['release'], )
            file_url = '{}/release-{}/gtf/{}/{}'.format(
                self.get_default_parameters()[self.CONFIG_KEY_DATA_DOWNLOADER][self.CONFIG_KEY_ENSEMBL_FTP][
                    self.CONFIG_KEY_BASE_URL], species['release'], species['name'], file_name)
            files.append(download_file(file_url, self.get_local_path_root_ensembl_repo() + '/' + file_name))
        except KeyError:
            self.get_logger().debug("No valid info is available species: ", species)

        return files


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
