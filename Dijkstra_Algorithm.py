import networkx as nx
import matplotlib.pyplot as plt

# Create a network graph
G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E"])
G.add_edges_from([("A", "B"), ("A", "C"), ("B", "D"),
                 ("C", "D"), ("C", "E"), ("D", "E")])

# Plot the network graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000,
        node_color='lightblue', font_size=12, font_weight='bold')
plt.title('Network Topology')

# Simulate packet forwarding
source = "A"
destination = "D"
shortest_path = nx.shortest_path(G, source=source, target=destination)
print("Shortest path from", source, "to", destination, ":", shortest_path)

# Animate packet forwarding
for i in range(len(shortest_path) - 1):
    plt.plot([pos[shortest_path[i]][0], pos[shortest_path[i + 1]][0]],
             [pos[shortest_path[i]][1], pos[shortest_path[i + 1]][1]],
             linestyle='dashed', color='red', alpha=0.5, linewidth=2)
    plt.text(pos[shortest_path[i]][0], pos[shortest_path[i]]
             [1] + 0.1, shortest_path[i], fontsize=12, ha='center')
    plt.pause(1)

plt.show()
