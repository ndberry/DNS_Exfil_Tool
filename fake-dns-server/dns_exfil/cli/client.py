import click

from dns_exfil.exfiltrators.chunkdownloader.cli import chunk_client
from dns_exfil.exfiltrators.botexfiltrator.cli import bot_client
from dns_exfil.exfiltrators.headerexecuter.cli import headerexecuter_client

@click.group()
def main():
    pass


main.add_command(bot_client)
main.add_command(chunk_client)
main.add_command(headerexecuter_client)
