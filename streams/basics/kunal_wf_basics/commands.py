import typer
from kunal_wf_basics.processing_functions import  upper_case
from kunal_wf_basics import  stream_functions
from kunal_wf_basics import  yaml_reader

from kunal_wf_basics import stream_adapter_functions

from typing import Iterator
app = typer.Typer()

@app.command()
def basic(input_file: str, output_file: str = None):
   
    upper_case(input_file, output_file)
    typer.echo(f"Processed {input_file} into {output_file or input_file + '.processed'}")


FUNCTION_LOOKUP = {
    "coalesce_empty_lines": stream_functions.coalesce_empty_lines,
    "break_lines": stream_functions.break_lines,
    "number_the_lines": stream_functions.number_the_lines,
    "stream_capitalize": stream_adapter_functions.stream_capitalize,
}

@app.command("process-stream")
def process_stream(
    input_file: str = typer.Argument(...),
    output_file: str = typer.Argument(...),
    config_file: str = typer.Option("pipeline.yaml", "--config", "-c")
):
    
 
    config = yaml_reader.read_config(config_file)
    pipeline_functions = config.get("pipeline", [])
    
    
    for func_name in pipeline_functions:
        if func_name not in FUNCTION_LOOKUP:
            typer.echo(f"Error: Function '{func_name}' is not recognized in the pipeline configuration.")
            raise typer.Exit(code=1)
    
 
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    lines_iter: Iterator[str] = iter(lines)
    
   
    for func_name in pipeline_functions:
        func = FUNCTION_LOOKUP[func_name]
        lines_iter = func(lines_iter)
    
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines_iter:
            outfile.write(line + "\n")
    
    typer.echo(f"Processing complete. Output written to '{output_file}'.")


if __name__ == "__main__":
    app()
