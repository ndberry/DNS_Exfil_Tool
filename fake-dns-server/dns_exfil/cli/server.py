from dns_exfil.exfiltrators.botexfiltrator.cli import bot
from dns_exfil.exfiltrators.chunkdownloader.cli import chunk
from dns_exfil.exfiltrators.headerexecuter.cli import headerexecuter
from dns_exfil.exfiltrators.base.server import start_server

import click


@click.group()
def main():
    pass

main.add_command(bot)
main.add_command(chunk)
main.add_command(headerexecuter)
