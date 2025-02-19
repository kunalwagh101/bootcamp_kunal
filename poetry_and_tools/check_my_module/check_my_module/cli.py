import typer

app = typer.Typer()

@app.command()
def greet(name: str = typer.Option(..., "--name", "-n", help="Your name")):
    """Simple CLI that greets the user."""
    print(f"Hello, {name}!")

if __name__ == "__main__":
    app()
