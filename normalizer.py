import ast

class ASTNormalizer(ast.NodeTransformer):
    """
    Traverses an AST and replaces specific names with generic placeholders
    to make the tree's structure comparable.
    """
    def visit_Name(self, node: ast.Name) -> ast.Name:
        """Normalizes variable names."""
        node.id = '_name_'
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Normalizes function names and their argument names."""
        node.name = '_func_'
        # Also normalize the arguments within the function definition
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg) -> ast.arg:
        """Normalizes function argument names."""
        node.arg = '_arg_'
        return node

# --- Example Usage ---
if __name__ == '__main__':
    from parser import parse_file_to_ast # Assuming parser.py is in the same directory

    # Create two logically identical but textually different files
    code1 = "def add(x, y):\n    result = x + y\n    return result"
    code2 = "def calculate(a, b):\n    answer = a + b\n    return answer"

    with open("file1.py", "w") as f: f.write(code1)
    with open("file2.py", "w") as f: f.write(code2)

    # 1. Parse both files into ASTs
    tree1 = parse_file_to_ast("file1.py")
    tree2 = parse_file_to_ast("file2.py")

    # 2. Create an instance of our normalizer
    normalizer = ASTNormalizer()

    # 3. Normalize both trees
    if tree1 and tree2:
        normalized_tree1 = normalizer.visit(tree1)
        normalized_tree2 = normalizer.visit(tree2)

        # 4. Compare the string dumps of the normalized trees
        dump1 = ast.dump(normalized_tree1)
        dump2 = ast.dump(normalized_tree2)

        print("Are the normalized ASTs identical?", dump1 == dump2) # Should print True
        print("\nNormalized AST Dump:")
        print(ast.dump(normalized_tree1, indent=4))