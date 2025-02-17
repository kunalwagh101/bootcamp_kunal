import sys
from pathlib import Path
import typer
import os
from typing import List
import logging
from many_hellos.helloworld import say_hello
app = typer.Typer()


@app.callback()
def main(verbose: bool = False):

    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
    else:
    
        logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")

@app.command()
def hello(
    names: List[str] = typer.Argument(...),
    config_logging: bool = typer.Option(False, help="Enable logging for the config loader only")
):
  
    logger_config = logging.getLogger("many_hellos._config_loder")
    if config_logging:
        logger_config.setLevel(logging.DEBUG)
    else:
        logger_config.setLevel(logging.WARNING)



    for name in names:
        print(say_hello(str(name)))

if __name__ == "__main__":
    app()
