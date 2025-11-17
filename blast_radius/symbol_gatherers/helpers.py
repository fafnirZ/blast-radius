# --- Helper Function to Check for Symbol in an Expression ---
import ast


def check_expression_contains_symbol(node: ast.expr, symbol: str, debug_recurse_level: int = 0) -> bool:
    """
    Recursively checks if the given AST expression node contains a name
    matching the target symbol's name.
    """
    if not isinstance(node, ast.AST) and debug_recurse_level == 0:
        raise RuntimeError("You passed in a null value, thats not allowed.")

    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
        # Check if the loaded name (a variable usage) matches the symbol's name
        if node.id == symbol:
            return True
    
    # Recursively check children nodes that are expressions
    for field, value in ast.iter_fields(node):
        # print(field)
        # print("val",value)
        if isinstance(value, ast.expr):
            if check_expression_contains_symbol(value, symbol, debug_recurse_level=debug_recurse_level+1):
                return True
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, ast.expr):
                    if check_expression_contains_symbol(item, symbol, debug_recurse_level=debug_recurse_level+1):
                        return True
      
    return False

