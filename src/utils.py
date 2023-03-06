"""Utils Functions"""


def print_hello_world_by_name(name="SomeOne") -> str:
    """Prints Hello World
    Args:
        name (str): Name of the person
    Returns:
        str
    """
    if name:
        return f"Hello World, {name}!"
    else:
        raise Exception("Name is empty")
