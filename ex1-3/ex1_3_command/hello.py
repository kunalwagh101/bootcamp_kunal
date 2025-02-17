import typer


app = typer.Typer()

@app.command()
def hello(name):
    print(f"hello {name}")

