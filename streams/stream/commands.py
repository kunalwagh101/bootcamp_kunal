#!/usr/bin/env python3
import typer
from stream import fib, get_str_range, str_range, skips

app = typer.Typer()


@app.command()
def fibonacci(n):
    typer.echo(fib(n))





@app.command()
def get_fibonacci():
   
    numbers = skips(skip=10, count=10)
    for num in numbers:
        typer.echo(num)

@app.command()
def str_range():
   
    lines = str_range(20)
    for line in lines:
        typer.echo(line)

@app.command()
def file_stream_command(filename: str):
  
    for line in get_str_range(filename):
        typer.echo(line)

if __name__ == "__main__":
    app()
