"""Use to upload data sets to the MetaGenScope web platform."""
import click

from metagenscope_cli.hello import hello
from metagenscope_cli.tools.metaphlan2 import metaphlan2
from metagenscope_cli.tools.kraken import kraken
from metagenscope_cli.tools.nanopore import nanopore
from metagenscope_cli.tools.microbe_census import microbe_census


@click.group()
def main():
    """Use to upload data sets to the MetaGenScope web platform."""
    pass


main.add_command(hello)
main.add_command(metaphlan2)
main.add_command(kraken)
main.add_command(nanopore)
main.add_command(microbe_census)
