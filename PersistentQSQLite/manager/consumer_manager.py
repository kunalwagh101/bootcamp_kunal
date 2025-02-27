import subprocess
import sys
import typer

app = typer.Typer()

@app.command()
def start_consumers(count: int = typer.Option(..., prompt="Enter the number of consumers to launch")):
    """
    Launch X consumer processes.
    """
    processes = []
    for i in range(count):

        process = subprocess.Popen(["poetry", "run", "python", "-m", "consumer.consumer"])
        processes.append(process)
        typer.echo(f"Started consumer process {i + 1} with PID {process.pid}")

    typer.echo("All consumer processes launched.")
    
    try:
      
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        typer.echo("Interrupt received. Terminating consumer processes...")
        for proc in processes:
            proc.terminate()
        sys.exit(0)

if __name__ == "__main__":
    app()
