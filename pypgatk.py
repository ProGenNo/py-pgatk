"""
This is the main tool that give access to all commands and options provided by the py-pgatk

@author ypriverol

"""
import logging
import click

from cgenomes.cbioportal_downloader import CbioPortalDownloadService
from ensembl.data_downloader import EnsemblDataDownloadService
from toolbox.exceptions import AppConfigException

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# Cli returns command line requests
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """This is the main tool that give access to all commands and options provided by the pypgatk"""


@cli.command()
@click.option('--config_file',
              '-c',
              help='Configuration file for the ensembl data downloader pipeline',
              default='config/ensembl_downloader_config.yaml')
@click.option('--output_directory',
              '-o',
              help='Output directory for the peptide databases',
              default="./database/")
@click.option('--folder_prefix_release',
              '-fp', help='Output folder prefix to download the data',
              default='release-')
@click.option('--taxonomy',
              '-t',
              help='Taxonomy List (comma separated) that will be use to download the data from Ensembl',
              default='')
@click.pass_context
def ensembl_downloader(ctx, config_file, output_directory, folder_prefix_release, taxonomy):
    """ This tool enables to download from enseml ftp the FASTA and GTF files"""

    if config_file is None:
        msg = "The config file for the pipeline is missing, please provide one "
        logging.error(msg)
        raise AppConfigException(msg)

    pipeline_arguments = {}
    if output_directory is not None:
        pipeline_arguments[EnsemblDataDownloadService._CONFIG_OUTPUT_DIRECTORY] = output_directory
    if folder_prefix_release is not None:
        pipeline_arguments[EnsemblDataDownloadService._CONFIG_KEY_FOLDER_PREFIX_RELEASE] = folder_prefix_release
    if taxonomy is not None:
        pipeline_arguments[EnsemblDataDownloadService._CONFIG_TAXONOMY] = taxonomy

    ensembl_download_service = EnsemblDataDownloadService(config_file, pipeline_arguments)

    logger = ensembl_download_service.get_logger_for("Main Pipeline Ensembl Downloader")
    logger.info("Pipeline STARTING ... ")

    ensembl_download_service.download_database_by_species()

    logger.info("Pipeline Finish !!!")


@cli.command()
@click.option('--config_file',
              '-c',
              help='Configuration file for the ensembl data downloader pipeline',
              default='config/cbioportal_downloader_config.yaml')
@click.option('--output_directory',
              '-o',
              help='Output directory for the peptide databases',
              default="./cbioportal/")
@click.option('--list_studies', '-l',
              help='Print the list of all the studies in cBioPortal (https://www.cbioportal.org)', is_flag=True)
@click.option('--download_study', '-d', help="Download an specific Study from cBioPortal -- (all to download all studies)")
@click.pass_context
def cbioportal_downloader(ctx, config_file, output_directory, list_studies, download_study):
    if config_file is None:
        msg = "The config file for the pipeline is missing, please provide one "
        logging.error(msg)
        raise AppConfigException(msg)

    pipeline_arguments = {}
    if output_directory is not None:
        pipeline_arguments[CbioPortalDownloadService._CONFIG_OUTPUT_DIRECTORY] = output_directory
    if list_studies is not None:
        pipeline_arguments[CbioPortalDownloadService._CONFIG_LIST_STUDIES] = list_studies

    cbioportal_downloader = CbioPortalDownloadService(config_file, pipeline_arguments)

    if list_studies is not None:
        list_studies = cbioportal_downloader.get_cancer_studies()
        print(list_studies)

    if download_study is not None:
        cbioportal_downloader.download_study(download_study)


if __name__ == "__main__":
    cli()
