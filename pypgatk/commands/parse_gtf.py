import os

import click

from pypgatk.commands.utils import print_help
from pypgatk.ensembl.ensembl import EnsemblDataService

this_dir, this_filename = os.path.split(__file__)

@click.command('parse-gtf', short_help="Generate the DB file from a GTF, to be used by the vcf-to-proteindb command")
@click.option('-c', '--config_file', help='Configuration to perform conversion between ENSEMBL Files',
              default=this_dir + '/../config/ensembl_config.yaml')
@click.option('-i', '--input_gtf', help='Path to the GTF file')
@click.option('-o', '--output_db', help='Path to the output DB file')
@click.pass_context

def parse_gtf(ctx, config_file, input_gtf, output_db):
  ensembl_data_service = EnsemblDataService(config_file, {})
  ensembl_data_service.parse_gtf(input_gtf, output_db)