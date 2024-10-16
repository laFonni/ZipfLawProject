import networkx as nx
import matplotlib.pyplot as plt

def load_neighbors_from_file(file_path):
    """
    Loads the word neighbors from a file where each line contains a word and its neighbors.
    
    Args:
    file_path (str): The path to the word neighbors file.
    
    Returns:
    dict: A dictionary where keys are words and values are sets of neighboring words.
    """
    neighbors = {}
    line_count = 0  # To keep track of the number of processed lines

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_count += 1  # Increment line count

                # Strip the line to avoid extra spaces
                line = line.strip()

                # Ensure the line is not empty
                if not line:
                    continue

                # Safely handle potential formatting errors
                if ": " in line:
                    word, neighbor_str = line.split(": ", 1)  # Split only at the first ": "
                    neighbor_list = neighbor_str.strip().split(", ")

                    # Add word and its neighbors to the dictionary
                    neighbors[word] = set(neighbor_list)
                else:
                    print(f"Skipping improperly formatted line: {line}")
                
                # Print progress every 1000 lines
                if line_count % 1000 == 0:
                    print(f"Processed {line_count} lines...")

        print(f"Finished processing {line_count} lines.")
    
    except Exception as e:
        print(f"Error occurred while processing file: {e}")
    
    return neighbors
    


def create_word_neighbor_graph(neighbors):
    """
    Creates a network graph of word neighbors using networkx.
    
    Args:
    neighbors (dict): A dictionary where keys are words and values are sets of neighboring words.
    
    Returns:
    networkx.Graph: A networkx graph object representing the word neighbors.
    """
    G = nx.Graph()
    
    # Add nodes and edges based on the word neighbors
    for word, neighbor_set in neighbors.items():
        G.add_node(word)
        for neighbor in neighbor_set:
            G.add_edge(word, neighbor)
    
    return G

import matplotlib.pyplot as plt
import networkx as nx

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Ellipse

def visualize_word_graph(G, output_file='word_neighbors_graph.png'):
    """
    Visualizes the word neighbor graph with horizontal oval nodes and saves it to a file.

    Args:
    G (networkx.Graph): The word neighbor graph.
    output_file (str): The file to save the graph image.
    """
    # Set up dark mode background for the plot
    plt.figure(figsize=(15, 15), facecolor='black')

    # Use circular_layout to position nodes on a circle
    pos = nx.circular_layout(G)

    # Dark mode colors
    node_color = '#106326'  # Soft blue nodes
    edge_color = '#cccccc'  # Light gray edges
    font_color = '#ffffff'  # White text for readability
    background_color = 'black'  # Black background

    # Draw edges first
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=0.8)

    ax = plt.gca()  # Get current axis

    # Draw nodes as horizontal ellipses (ovals)
    for node in G.nodes:
        x, y = pos[node]
        ellipse = Ellipse((x, y), width=0.12, height=0.1, angle=0, color=node_color, linewidth=1.5, edgecolor="gray")
        ax.add_patch(ellipse)

    # Draw the labels for the nodes
    nx.draw_networkx_labels(G, pos, font_size=10, font_color=font_color, font_weight='bold')

    # Set the background color of the plot
    plt.gca().set_facecolor(background_color)

    # Save the graph image to file
    plt.savefig(output_file, facecolor=background_color)
    print(f"Graph saved as {output_file}")

    # Show the graph
    plt.show()



def generate_graphs():
    # Load neighbors from the file
    file_path = "filtered_word_neighbors.txt"  # Replace with the actual path to your file
    neighbors = load_neighbors_from_file(file_path)

    # Create the graph from word neighbors
    G = create_word_neighbor_graph(neighbors)
    
    # Visualize and save the graph
    visualize_word_graph(G, output_file='word_neighbors_graph.png')