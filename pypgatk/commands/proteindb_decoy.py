import logging

import click

from pypgatk.proteomics.db.decoy_pyrat import ProteinDBService
from pypgatk.toolbox.exceptions import AppConfigException


@click.command('generate-decoy', short_help='Create decoy protein sequences. Each protein '
                                             'is reversed and the cleavage sites switched with preceding amino acid. Peptides are checked for existence in target sequences if found'
                                             'the tool will attempt to shuffle them. James.Wright@sanger.ac.uk 2015')
@click.option('--config_file', '-c', help='Configuration file for the protein database decoy generation',
              default='config/protein_decoy.yaml')
@click.option('--output', '-o', help='Output file for decoy database',
              default="protein-decoy.fa")
@click.option('--input','-i',  metavar='*.fasta|*.fa', help='FASTA file of target proteins sequences for which to'
                                                            ' create decoys')
@click.option('--cleavage_sites', '-c', default='KR',
                    help='A list of amino acids at which to cleave during digestion. Default = KR')
@click.option('--anti_cleavage_sites', '-a', dest='noc', default='',
                    help='A list of amino acids at which not to cleave if following cleavage site ie. Proline. Default = none')
@click.option('--cleavage_position', '-p', dest='cpos', default='c', choices=['c', 'n'],
                    help='Set cleavage to be c or n terminal of specified cleavage sites. Default = c')
@click.option('--min_peptide_length', '-l', dest='minlen', default=5, type=int,
                    help='Set minimum length of peptides to compare between target and decoy. Default = 5')
@click.option('--max_iterations', '-n', dest='maxit', default=100, type=int,
                    help='Set maximum number of times to shuffle a peptide to make it non-target before failing. Default=100')
@click.option('--do_not_shuffle', '-x', dest='noshuf', default=False, action='store_true',
                    help='Turn OFF shuffling of decoy peptides that are in the target database. Default=false')
@click.option('--do_not_switch', '-s', dest='noswitch', default=False, action='store_true',
                    help='Turn OFF switching of cleavage site with preceding amino acid. Default=false')
@click.option('--decoy_prefix', '-d', dest='dprefix', default='XXX',
                    help='Set accession prefix for decoy proteins in output. Default=XXX')
@click.option('--temp_file', '-t', dest='tout', default='tmp.fa',
                    help='Set temporary file to write decoys prior to shuffling. Default=tmp.fa')
@click.option('--no_isobaric', '-b', dest='iso', default=False, action='store_true',
                    help='Do not make decoy peptides isobaric. Default=false')
@click.option('--memory_save', '-m', dest='mem', default=False, action='store_true',
                    help='Slower but uses less memory (does not store decoy peptide list). Default=false')
@click.pass_context
def generate_database(ctx, config_file, output, input, cleavage_sites, anti_cleavages_sites, cleavage_position, min_peptide_length,
                   max_interactions, do_not_shuffle, do_not_switch, decoy_prefix, temp_file, no_isobaric, memory_save):

    if config_file is None:
        msg = "The config file for the pipeline is missing, please provide one "
        logging.error(msg)
        raise AppConfigException(msg)

    pipeline_arguments = {}

    if output is not None:
        pipeline_arguments[ProteinDBService.CONFIG_PROTEINDB_OUTPUT] = output

    if input is not None:
        pipeline_arguments[ProteinDBService.CONFIG_INPUT_FILE] = input

    if cleavage_position is not None:
        pipeline_arguments[ProteinDBService.CONFIG_CLEAVAGE_SITES] = cleavage_sites

    if cleavage_position is not None:
        pipeline_arguments[ProteinDBService.CONFIG_CLEAVAGE_POSITION] = cleavage_position

    if anti_cleavages_sites is not None:
        pipeline_arguments[ProteinDBService.CONFIG_ANTI_CLEAVAGE_SITES] = anti_cleavages_sites

    if min_peptide_length is not None:
        pipeline_arguments[ProteinDBService.CONFIG_PEPTIDE_LENGTH] = min_peptide_length

    if max_interactions is not None:
        pipeline_arguments[ProteinDBService.CONFIG_MAX_ITERATIONS] = max_interactions

    if do_not_shuffle is not None:
        pipeline_arguments[ProteinDBService.CONFIG_DO_NOT_SUFFLE] = do_not_shuffle

    if do_not_switch is not None:
        pipeline_arguments[ProteinDBService.CONFIG_DO_NOT_SWITCH] = do_not_switch

    if decoy_prefix is not None:
        pipeline_arguments[ProteinDBService.CONFIG_DECOY_PREFIX] = decoy_prefix

    if temp_file is not None:
        pipeline_arguments[ProteinDBService.CONFIG_TEMP_FILE] = temp_file

    if no_isobaric is not None:
        pipeline_arguments[ProteinDBService.CONFIG_NO_ISOBARIC] = no_isobaric

    if memory_save is not None:
        pipeline_arguments[ProteinDBService.CONFIG_MEMORY_SAVE] = memory_save

    proteindb_decoy = ProteinDBService(config_file, pipeline_arguments)
    proteindb_decoy.decoy_database()
