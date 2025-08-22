import typer
from .config import app

@app.command()
def greet(name: str):
    """Say hello to someone."""
    typer.echo(f"Hello, {name}!")

@app.command()
def add(a: int, b: int):
    """Add two numbers."""
    typer.echo(f"Result: {a + b}")

if __name__ == "__main__":
    app()
