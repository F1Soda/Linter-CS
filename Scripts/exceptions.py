import networkx as nx
from Utils import Token


class NodeInGraphNotFound(Exception):
    def __init__(self, token: Token, graph_name: str):
        message = f"Couldn't find token {token} in {graph_name} graph."
        super().__init__(message)


class GraphNotFound(Exception):
    def __init__(self, graph: nx.DiGraph):
        message = f"Couldn't find {str(graph)} graph in linter's graphs."
        super().__init__(message)


class ErrorInLinterTest(Exception):
    def __init__(self, link_to_file: str):
        message = f"Was error in linter. File: {link_to_file}"
        super().__init__(message)


class UnexpectedChar(Exception):
    def __init__(self, char: str, excerpt: str):
        message = "Undefined char = " + f'"{char}"\nLine was:' + f"...{excerpt}..."
        super().__init__(message)
