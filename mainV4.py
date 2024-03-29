import re


def parse_dot_content(content):
    connections = re.findall(r'\s*(\w+)\s*->\s*(\w+)\s*\[label="([^"]*)"\s*color="([^"]*)"\];', content)
    nodes = re.findall(r'\s*(\w+)\s*\[label\s*=\s*"([^"]*)"\];', content)
    return {
        'connections': connections,
        'nodes': nodes
    }


def create_graph(graph, table_names):
    table_names_lower = [name.lower() for name in table_names]
    graph_str = 'digraph FilteredGraph {\n  node [shape=record];\n'

    for node, label in graph['nodes']:
        if any(table_name in node.lower() for table_name in table_names_lower):
            graph_str += f'  {node}   [label = "{label}"];\n'

    for source, target, label, color in graph['connections']:
        if any(table_name in source.lower() or table_name in target.lower() for table_name in table_names_lower):
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

    # Specify the table names to filter
    table_names = ['transaction_payment_response', 'transaction_payment_response_status','debt','channel','transaction_type','transaction_provider','transaction_channel_type','offer_group_interval','campaign_run_debt','campaign_run','customer','payment_method']  # Add the table names you want to filter here

    graph = parse_dot_content(content)
    graph_str = create_graph(graph, table_names)

    # Print the output to the console
    print(graph_str)


if __name__ == "__main__":
    main()
