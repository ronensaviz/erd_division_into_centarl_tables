import re
from collections import defaultdict


def read_dot_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def parse_dot_content(content):
    # Extracting all edges and their labels
    edges = re.findall(r'(\w+)\s*->\s*(\w+)(?:\s*\[label="([^"]*)"\])?', content)

    # Building a graph and identifying central tables
    graph = defaultdict(list)
    central_tables = set()
    for src, dest, label in edges:
        graph[src].append((dest, label))
        central_tables.add(src)

    return graph, central_tables


def create_subgraphs(graph, central_tables):
    subgraphs = {}
    for central in central_tables:
        subgraph = []
        subgraph.append(f'digraph {central}Architecture {{')

        # Adding nodes with specific shapes
        for dest, label in graph[central]:
            subgraph.append(f'  {central}')
            subgraph.append(f'  {dest}[shape=rectangle]')  # Adjust the shape as per your requirement

            # Adding edges with labels
            edge = f'  {central} -> {dest}'
            if label:
                edge += f'[label="{label}"]'
            edge += ';'
            subgraph.append(edge)

        subgraph.append('}')
        subgraphs[central] = '\n'.join(subgraph)
    return subgraphs


def main():
    file_path = '/Users/ronen_saviz/PycharmProjects/erd_division_into_centarl_tables/digraph_erd.dot'  # Replace with the path to your DOT file
    content = read_dot_file(file_path)
    graph, central_tables = parse_dot_content(content)
    subgraphs = create_subgraphs(graph, central_tables)

    # Printing the subgraphs
    for central, subgraph in subgraphs.items():
        print(subgraph)
        print()


if __name__ == "__main__":
    main()
