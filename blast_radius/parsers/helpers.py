# --- Helper Function to Check for Symbol in an Expression ---
import ast


def check_expression_contains_symbol(node: ast.expr, symbol: str) -> bool:
    """
    Recursively checks if the given AST expression node contains a name
    matching the target symbol's name.
    """
    if node is None:
        return False
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        # Check if the loaded name (a variable usage) matches the symbol's name
        if node.id == symbol:
            return True
    
    # Recursively check children nodes that are expressions
    for field, value in ast.iter_fields(node):
        if isinstance(value, ast.expr):
            if check_expression_contains_symbol(value, symbol):
                return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.expr):
                    if check_expression_contains_symbol(item, symbol):
                        return True
    return False

