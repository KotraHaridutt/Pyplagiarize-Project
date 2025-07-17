import ast
from zss import simple_distance


# ADD: Helper function to get children from an AST node
def get_children(node: ast.AST):
    """
    Returns an iterable of the direct child nodes of an AST node.
    """
    return list(ast.iter_child_nodes(node))


# ADD: Helper function to get a label for an AST node
def get_label(node: ast.AST):
    """
    Returns a string label for an AST node, using its class name.
    """
    return node.__class__.__name__


def get_node_count(node: ast.AST) -> int:
    """
    Counts the total number of nodes in an AST.
    """
    return sum(1 for _ in ast.walk(node))


def calculate_similarity(tree1: ast.AST, tree2: ast.AST) -> float:
    """
    Calculates the structural similarity between two ASTs.
    """
    if not tree1 or not tree2:
        return 0.0

    # UPDATE: Pass the helper functions to simple_distance
    distance = simple_distance(
        tree1,
        tree2,
        get_children=get_children,
        get_label=get_label
    )

    nodes1 = get_node_count(tree1)
    nodes2 = get_node_count(tree2)
    max_distance = nodes1 + nodes2

    if max_distance == 0:
        return 1.0

    similarity = 1 - (distance / max_distance)

    return similarity


# --- Example Usage (no changes needed here) ---
if __name__ == '__main__':
    from parser import parse_file_to_ast
    from normalizer import ASTNormalizer

    code1 = "def add(x, y):\n    return x + y"
    code2 = "def compute(val1, val2):\n    return val1 + val2"
    code3 = "class MyClass:\n    pass"

    with open("file1.py", "w") as f: f.write(code1)
    with open("file2.py", "w") as f: f.write(code2)
    with open("file3.py", "w") as f: f.write(code3)

    normalizer = ASTNormalizer()
    norm_tree1 = normalizer.visit(parse_file_to_ast("file1.py"))
    norm_tree2 = normalizer.visit(parse_file_to_ast("file2.py"))
    norm_tree3 = normalizer.visit(parse_file_to_ast("file3.py"))

    similarity_1_2 = calculate_similarity(norm_tree1, norm_tree2)
    similarity_1_3 = calculate_similarity(norm_tree1, norm_tree3)

    print(f"Similarity between file1.py and file2.py: {similarity_1_2:.2f}")
    print(f"Similarity between file1.py and file3.py: {similarity_1_3:.2f}")