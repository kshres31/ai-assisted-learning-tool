import ast


class UnsafeCodeError(ValueError):
    pass


_ALLOWED_ATTRIBUTES = {
    "add",
    "append",
    "count",
    "get",
    "items",
    "join",
    "keys",
    "lower",
    "pop",
    "split",
    "strip",
    "upper",
    "values",
}
_BLOCKED_NODES = (ast.ClassDef, ast.Global, ast.Import, ast.ImportFrom, ast.Nonlocal)
_BLOCKED_CALLS = {
    "breakpoint",
    "compile",
    "delattr",
    "dir",
    "eval",
    "exec",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "open",
    "setattr",
    "vars",
}


def validate_student_code(code: str) -> ast.Module:
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as error:
        message = error.msg or "Invalid Python syntax"
        raise UnsafeCodeError(f"Syntax error on line {error.lineno}: {message}") from error

    for node in ast.walk(tree):
        if isinstance(node, _BLOCKED_NODES):
            raise UnsafeCodeError(f"{type(node).__name__} is not allowed in exercise code")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            raise UnsafeCodeError("Double-underscore names are not allowed")
        if isinstance(node, ast.Attribute) and node.attr not in _ALLOWED_ATTRIBUTES:
            raise UnsafeCodeError(f"Attribute '{node.attr}' is not allowed")
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in _BLOCKED_CALLS
        ):
            raise UnsafeCodeError(f"Call to '{node.func.id}' is not allowed")
    return tree
