import typer
from typing import List
from helloworld import say_hello

app = typer.Typer()

@app.command()
def view(names:List[str]= typer.Argument(...)) :
    say_hello(names)


if __name__ == "__main__":
    app()
   