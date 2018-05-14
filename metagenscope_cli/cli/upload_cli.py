"""CLI to upload data to a MetaGenScope Server."""

import click
import click_log

from metagenscope_cli.extensions import logger
from metagenscope_cli.sample_sources.data_super_source import DataSuperSource
from metagenscope_cli.sample_sources.file_source import FileSource

from .utils import batch_upload, add_authorization, parse_metadata


@click.group()
def upload():
    """Handle different types of uploads."""
    pass


@upload.command()
@click_log.simple_verbosity_option(logger)
@add_authorization()
@click.argument('metadata_csv')
@click.argument('sample_names', nargs=-1)
def metadata(uploader, metadata_csv, sample_names):
    """Upload a CSV metadata file."""
    parsed_metadata = parse_metadata(metadata_csv, sample_names)
    for sample_name, metadata_dict in parsed_metadata.items():
        payload = {
            'sample_name': str(sample_name),
            'metadata': metadata_dict,
        }
        try:
            response = uploader.knex.post('/api/v1/samples/metadata', payload)
            logger.info(response)
        except Exception:  # pylint:disable=broad-except
            logger.error(f'[upload-metadata-error] {sample_name}')


@upload.command()
@click_log.simple_verbosity_option(logger)
@add_authorization()
@click.option('-g', '--group', default=None)
@click.option('--group-name', default=None)
def datasuper(uploader, group, group_name):
    """Upload all samples from DataSuper repo."""
    sample_source = DataSuperSource()
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group, upload_group_name=group_name)


@upload.command()
@click_log.simple_verbosity_option(logger)
@add_authorization()
@click.option('-g', '--group', default=None)
@click.argument('result_files', nargs=-1)
def files(uploader, group, result_files):
    """Upload all samples from llist of tool result files."""
    sample_source = FileSource(files=result_files)
    samples = sample_source.get_sample_payloads()

    batch_upload(uploader, samples, group_uuid=group)
