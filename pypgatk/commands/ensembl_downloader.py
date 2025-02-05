## File modified by Jakub Vasicek (jakub.vasicek@uib.no)

import logging
import os

import click

from pypgatk.ensembl.data_downloader import EnsemblDataDownloadService
from pypgatk.toolbox.exceptions import AppConfigException

this_dir, this_filename = os.path.split(__file__)


@click.command('ensembl-downloader', short_help='Command to download the ensembl information')
@click.option('-c', '--config_file',
              help='Configuration file for the ensembl data downloader pipeline',
              default=this_dir + '/../config/ensembl_downloader_config.yaml')
@click.option('-o', '--output_directory',
              help='Output directory for the peptide databases',
              default="./database_ensembl/")
@click.option('-fp', '--folder_prefix_release',
              help='Output folder prefix to download the data',
              default='release-')
@click.option('-t', '--taxonomy',
              help='Taxonomy identifiers (comma separated list can be given) that will be use to download the data from Ensembl',
              default='')
@click.option('-l', '--list_taxonomies',
              help='Print the list of all the taxonomies in ENSEMBL (https://www.ensembl.org)', is_flag=True,
              default=False)
@click.option('-sg', '--skip_gtf', help="Skip the gtf file during the download", is_flag=True)
@click.option('-sp', '--skip_protein', help="Skip the protein fasta file during download", is_flag=True)
@click.option('-sc', '--skip_cds', help='Skip the CDS file download', is_flag=True)
@click.option('-scd', '--skip_cdna', help='Skip the cDNA file download', is_flag=True)
@click.option('-sn', '--skip_ncrna', help='Skip the ncRNA file download', is_flag=True)
@click.option('-sd', '--skip_dna', help='Skip the DNA (reference genome assembly) file download', is_flag=True)
@click.option('-sv', '--skip_vcf', help='Skip the VCF variant file', is_flag=True)
@click.option('-vchr', '--vcf_chr', help='Specify which chromosome VCF to download. Give a comma-separated list (e.g. 1,2,3,X,MT), or "all" (default value).', default='all')
@click.option('-en', '--ensembl_name',
              help='Ensembl name code to download, it can be use instead of taxonomy (e.g. homo_sapiens)', default='')
@click.option('--grch37', help='Download a previous version GRCh37 of ensembl genomes', is_flag=True)
@click.option('-nu', '--no_unzip', help='Do not run gunzip after download (files have to be unzipped manually afterwards)', is_flag=True)
@click.option('-v', '--verbous', help='Display which files are being downloaded', is_flag=True)
def ensembl_downloader(config_file, output_directory, folder_prefix_release,
                       taxonomy, list_taxonomies, skip_gtf, skip_protein,
                       skip_cds, skip_cdna, skip_ncrna, skip_dna, skip_vcf, vcf_chr,
                       ensembl_name, grch37=False, no_unzip=False, verbous=False):
  """ This tool enables to download from enseml ftp the FASTA and GTF files"""
  
  if verbous:
    print("[Ensembl Downloader]: Downloading files for ", end='')
    if taxonomy is not None and taxonomy != '':
        print(taxonomy)
    elif ensembl_name is not None:
        print(ensembl_name)
        
    print("[Ensembl Downloader]: Options: ", end='')
    if skip_protein is not None and skip_protein:
        print("--skip_protein", end=' ')
    if skip_gtf is not None and skip_gtf:
        print("--skip_gtf", end=' ')
    if skip_cds is not None and skip_cds:
        print("--skip_cds", end=' ')
    if skip_cdna is not None and skip_cdna:
        print("--skip_cdna", end=' ')
    if skip_ncrna is not None and skip_ncrna:
        print("--skip_ncrna", end=' ')
    if skip_dna is not None and skip_dna:
        print("--skip_dna", end=' ')
    if skip_vcf is not None and skip_vcf:
        print("--skip_vcf", end=' ')
    print("")

  if config_file is None:
    msg = "The config file for the pipeline is missing, please provide one "
    logging.error(msg)
    raise AppConfigException(msg)

  # Parse pipelines parameters.
  pipeline_arguments = {}
  if output_directory is not None:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_OUTPUT_DIRECTORY] = output_directory
  if folder_prefix_release is not None:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_FOLDER_PREFIX_RELEASE] = folder_prefix_release
  if taxonomy is not None:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_TAXONOMY] = taxonomy
  if ensembl_name is not None:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_ENSEMBL_NAME] = ensembl_name
  if list_taxonomies:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_LIST_TAXONOMIES] = list_taxonomies
  if skip_protein is not None and skip_protein:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_PROTEIN] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_PROTEIN] = False
  if skip_gtf is not None and skip_gtf:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_GTF] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_GTF] = False
  if skip_cds is not None and skip_cds:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_CDS] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_CDS] = False
  if skip_ncrna is not None and skip_ncrna:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_NCRNA] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_NCRNA] = False
  if skip_dna is not None and skip_dna:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_DNA] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_DNA] = False
  if skip_cdna is not None and skip_cdna:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_CDNA] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_CDNA] = False
  if skip_vcf is not None and skip_vcf:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_VCF] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_SKIP_VCF] = False
  if no_unzip is not None and no_unzip:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_NO_UNZIP] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_NO_UNZIP] = False
  if verbous is not None and verbous:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_VERBOUS] = True
  else:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_VERBOUS] = False
  if vcf_chr is not None:
    pipeline_arguments[EnsemblDataDownloadService.CONFIG_KEY_VCF_CHR] = vcf_chr


  ensembl_download_service = EnsemblDataDownloadService(config_file, pipeline_arguments)

  logger = ensembl_download_service.get_logger_for("Main Pipeline Ensembl Downloader")
  logger.info("Pipeline STARTING ... ")
  if list_taxonomies:
    list_of_taxonomies = ensembl_download_service.get_species_from_rest()
    for taxonomy_info in list_of_taxonomies:
      print(taxonomy_info)

  ensembl_download_service.download_database_by_species(grch37)

  logger.info("Pipeline Finish !!!")
