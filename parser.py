import ast

def parse_file_to_ast(file_path: str):
    """
    Reads a Python file and parses it into an Abstract Syntax Tree.

    Args:
        file_path: The path to the Python source file.

    Returns:
        An ast.Module object representing the root of the AST, or None if parsing fails.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
            # The core parsing step
            tree = ast.parse(source_code, filename=file_path)
            return tree
    except (FileNotFoundError, SyntaxError) as e:
        print(f"Error parsing {file_path}: {e}")
        return None

# --- Example Usage ---
if __name__ == '__main__':
    # Create a dummy file to test
    dummy_code = "def my_func(a, b):\n    c = a + b\n    return c"
    with open("test.py", "w") as f:
        f.write(dummy_code)

    # Parse the file and see the AST
    ast_tree = parse_file_to_ast("test.py")
    if ast_tree:
        # ast.dump provides a detailed string representation of the tree
        print("Successfully parsed file. AST representation:")
        print(ast.dump(ast_tree, indent=4))