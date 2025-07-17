# In src/main.py

import typer
import ast
from pathlib import Path
from itertools import product
from typing_extensions import Annotated
from typing import List, Union

# Import your existing modules
from parser import parse_file_to_ast
from normalizer import ASTNormalizer
from similarity import calculate_similarity

app = typer.Typer(help="PyPlagiarize: An AST-based code similarity detector for Python.")

# Define a type for Function or Class definitions
Definition = Union[ast.FunctionDef, ast.ClassDef]


def get_definitions(tree: ast.Module) -> List[Definition]:
    """Extracts all top-level function and class definitions from an AST."""
    return [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]


@app.command()
def check(
        path1: Annotated[Path, typer.Argument(exists=True, help="Path to the first Python file.")],
        path2: Annotated[Path, typer.Argument(exists=True, help="Path to the second Python file.")],
        threshold: Annotated[float, typer.Option(help="Similarity threshold (0.0 to 1.0) to report plagiarism.")] = 0.8
):
    """
    Compares functions and classes between two Python files to find similarities.
    """
    if not (path1.is_file() and path2.is_file()):
        typer.secho("Error: Both paths must be files.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo(f"Comparing definitions in '{path1.name}' and '{path2.name}'...")

    # Parse files and extract definitions
    tree1 = parse_file_to_ast(str(path1))
    tree2 = parse_file_to_ast(str(path2))

    if not tree1 or not tree2:
        raise typer.Exit(code=1)

    defs1 = get_definitions(tree1)
    defs2 = get_definitions(tree2)

    if not defs1 or not defs2:
        typer.echo("No top-level functions or classes found to compare.")
        raise typer.Exit()

    normalizer = ASTNormalizer()
    found_plagiarism = False

    # Compare every pair of definitions
    for def1, def2 in product(defs1, defs2):
        # Normalize copies of the subtrees for comparison
        norm_def1 = normalizer.visit(def1)
        norm_def2 = normalizer.visit(def2)

        similarity = calculate_similarity(norm_def1, norm_def2)

        if similarity >= threshold:
            found_plagiarism = True
            def_type = "Function" if isinstance(def1, ast.FunctionDef) else "Class"

            report = f"\n[{similarity:.2%}] High similarity found for {def_type}:"
            typer.secho(report, fg=typer.colors.RED, bold=True)
            typer.echo(f" - '{def1.name}' in {path1.name} (line {def1.lineno})")
            typer.echo(f" - '{def2.name}' in {path2.name} (line {def2.lineno})")

    if not found_plagiarism:
        typer.secho("\n✅ No similar code blocks found above the threshold.", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()