import typer
from hello import say_hello

app = typer.Typer()

@app.command()
def hello(name: str):
    """Prints a greeting."""
    print(say_hello(name))
    # print(f" hello {name}")

if __name__ == "__main__":
    app()
