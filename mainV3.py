import re
from collections import defaultdict


def read_dot_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content


def parse_dot_content(content):
    edges = re.findall(r'(\w+)\s*->\s*(\w+)(?:\s*\[label="([^"]*)"\])?', content)
    graph = defaultdict(list)
    for src, dest, label in edges:
        graph[src].append((dest, label))
    return graph


def traverse_graph(graph, central_table_name):
    connected_graph = defaultdict(list)

    for node in graph.keys():
        if central_table_name in node:
            for dest, label in graph[node]:
                if central_table_name in dest:  # Only add relationships where both nodes contain central_table_name as a substring
                    connected_graph[node].append((dest, label))

    return connected_graph


def create_graph(graph):
    graph_str_list = ['digraph Architecture {']

    for src, edges in graph.items():
        graph_str_list.append(f'  {src}[shape=rectangle]')
        for dest, label in edges:
            edge = f'  {src} -> {dest}'
            if label:
                edge += f'[label="{label}"]'
            edge += ';'
            graph_str_list.append(edge)

    graph_str_list.append('}')
    return '\n'.join(graph_str_list)


def main():
    central_table_name = "transaction"  # Replace with the substring of your central table
    file_path = '/Users/ronen_saviz/PycharmProjects/erd_division_into_centarl_tables/digraph_erd.dot'  # Replace with the path to your DOT file

    content = read_dot_file(file_path)
    graph = parse_dot_content(content)

    connected_graph = traverse_graph(graph, central_table_name)
    graph_str = create_graph(connected_graph)

    print(graph_str)


if __name__ == "__main__":
    main()
