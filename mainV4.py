import re


def parse_dot_content(content):
    connections = re.findall(r'\s*(\w+)\s*->\s*(\w+)\s*\[label="([^"]*)"\s*color="([^"]*)"\];', content)
    nodes = re.findall(r'\s*(\w+)\s*\[label\s*=\s*"([^"]*)"\];', content)
    return {
        'connections': connections,
        'nodes': nodes
    }


def create_graph(graph, table_name):
    table_name_lower = table_name.lower()
    graph_str = f'digraph {table_name} {{\n  node [shape=record];\n'

    for node, label in graph['nodes']:
        if table_name_lower in node.lower():
            graph_str += f'  {node}   [label = "{label}"];\n'

    for source, target, label, color in graph['connections']:
        if table_name_lower in source.lower() or table_name_lower in target.lower():
            corrected_label = label.replace('UNKNOWN', f'{source}_id (JOIN)')
            graph_str += f'  {source} -> {target} [label="{corrected_label}" color="{color}"];\n'

    graph_str += '}'
    return graph_str


def main():
    # Specify the path to your .dot file
    file_path = 'digraph_erd.dot'

    # Read the content of the .dot file
    with open(file_path, 'r') as file:
        content = file.read()

    # Specify the table name to filter
    table_name = 'נםםל'

    graph = parse_dot_content(content)
    graph_str = create_graph(graph, table_name)

    # Print the output to the console
    print(graph_str)


if __name__ == "__main__":
    main()
