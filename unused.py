import ast


def identify_unused(tree):
    used_names = set()
    imported_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.add(extract_aliased_name(alias))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.add(extract_aliased_name(alias))
        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    return imported_names - used_names


def extract_aliased_name(alias):
    if alias.asname is None:
        return alias.name
    else:
        return alias.asname
