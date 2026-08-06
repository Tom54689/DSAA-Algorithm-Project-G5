"""
Question 1 : Greedy algorithm
Problem Scenario: Minimum-Cost MRT Network in Rural Sarawak


You are an urban transport developer responsible for planning the early stages of an MRT network in rural Sarawak. Due to limited funding, it is not possible to build every proposed connection between the MRT stations.
Each MRT station is represented as a point, while every possible connection between two stations has an estimated construction cost (edge's weight). 
Your task is to determine which connections should be built so that all MRT stations are connected at the minimum possible total cost.


1) user enters number of vertices, edges, starting/ending vertex and edges' weight for graph.
2) Selection Sort arrange edges in ascending order
3) Disjoint Set is used to determine whether adding the current lowest weight edge will create a cycle..
4) The process stops when (V-1) edges have been selected.
"""

import os
def read_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")

#vertex must be integer
def read_vertex(prompt, vertices):
    while True:
        vertex = read_integer(prompt)

        if 1 <= vertex <= vertices:
            return vertex

        print(f"Vertex must be between 1 and {vertices}.")


# can be a floating number
def read_weight():
    while True:
        try:
            weight = float(input("Weight: "))

            if weight < 0:
                print("Weight cannot be negative.")
            else:
                return weight

        except ValueError:
            print("Please enter a valid number.")


def read_number_of_vertices():
    while True:
        vertices = read_integer("Enter the number of vertices: ")

        if vertices < 2:
            print("At least 2 vertices are required.")
        else:
            return vertices

# the formula to find the max number of edges in an undirected graph is n * (n - 1) / 2
def read_number_of_edges(vertices):
    minimum = vertices - 1
    maximum = vertices * (vertices - 1) // 2

    print(f"For {vertices} vertices, enter between {minimum} and {maximum} edges.")

    while True:
        edges = read_integer("Enter the number of edges: ")

        if edges < minimum:
            print(f"Please enter at least {minimum} edges")
        elif edges > maximum:
            print(f"Please enter a maximum of {maximum} edges")
        else:
            return edges


# The program collects each edge in the format [starting vertex, ending vertex, weight] and stores all edges in a list of lists called edges
def read_edges(vertices, number_of_edges):
    edges = []

    while len(edges) < number_of_edges:
        print(f"\nEdge {len(edges) + 1}")
        start = read_vertex("Start vertex: ", vertices)
        end = read_vertex("End vertex: ", vertices)

        if start == end:
            print("An edge cannot connect a vertex to itself.")
            continue

        if edge_exists(edges, start, end):
            print("That undirected edge already exists.")
            continue

        weight = read_weight()
        edges.append([start, end, weight])

    return edges

# check whether the edge already exist between the two vertices
def edge_exists(edges, start, end):
    for existing_start, existing_end, weight in edges:
        if ((existing_start == start and existing_end == end) or
                (existing_start == end and existing_end == start)):
            return True
    return False

# UI function to display edges in a table format
def display_edges(title, edges):
    print(f"\n{title}")
    print("-" * 42)
    print(f"{'Start':<10}{'End':<10}{'Weight':>12}")
    print("-" * 42)

    for start, end, weight in edges:
        print(f"{start:<10}{end:<10}{weight:>12g}")

    print("-" * 42)


def kruskal(vertices, edges):
    sorted_edges = selection_sort_edges(edges)

    mst_graph = {}

    for vertex in range(1, vertices + 1):
        mst_graph[vertex] = []

    mst = []
    total_weight = 0.0

    for start, end, weight in sorted_edges:

        if creates_cycle(mst_graph, start, end):
            print(f"({start}, {end}, {weight:g}) - no cycle (selected)")
        else:
            print(f"({start}, {end}, {weight:g}) - forms a cycle (skipped)")

            mst.append([start, end, weight])
            total_weight += weight

            mst_graph[start].append(end)
            mst_graph[end].append(start)

        #stop the loop once n - 1 edges have been selected
        if len(mst) == vertices - 1:
            break

    return mst, total_weight

#arrange the edges in ascending order
def selection_sort_edges(edges):
    sorted_edges = [edge.copy() for edge in edges]

    for current in range(len(sorted_edges) - 1):
        minimum = current

        for comparison in range(current + 1, len(sorted_edges)):
            if sorted_edges[comparison][2] < sorted_edges[minimum][2]:
                minimum = comparison

        if minimum != current:
            temp = sorted_edges[current]
            sorted_edges[current] = sorted_edges[minimum]
            sorted_edges[minimum] = temp

    return sorted_edges


#purpose of this function is to determine whether the current edge creates a cycle using DFS  to determine if a path alr exist
def has_path(graph, current_vertex, target_vertex, visited):
    if current_vertex == target_vertex:
        return True

    visited.add(current_vertex)

    for neighbour in graph[current_vertex]:
        if neighbour not in visited:
            if has_path(graph, neighbour, target_vertex, visited):
                return True

    return False


def creates_cycle(graph, start_vertex, end_vertex):
    return has_path(
        graph,
        start_vertex,
        end_vertex,
        set()
    )


def display_edges(title, edges):
    print(f"\n{title}")
    print("-" * 42)
    print(f"{'Start':<10}{'End':<10}{'Weight':>12}")
    print("-" * 42)

    for start, end, weight in edges:
        print(f"{start:<10}{end:<10}{weight:>12g}")

    print("-" * 42)


def display_result(vertices, mst, total_weight):
    if len(mst) != vertices - 1:
        print("\nNo Minimum Spanning Tree")
        return

    display_edges("Minimum Spanning Tree", mst)
    print(f"Minimum total weight: {total_weight:g}")


def main():
    
    print("=" * 62)
    print("KRUSKAL'S ALGORITHM")
    print("=" * 62)

    vertices = read_number_of_vertices()
    number_of_edges = read_number_of_edges(vertices)
    edges = read_edges(vertices, number_of_edges)

    display_edges("Edges Entered", edges)
    mst, total_weight = kruskal(vertices, edges)
    display_result(vertices, mst, total_weight)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram stopped ")