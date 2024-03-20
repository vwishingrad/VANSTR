import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask the user to select the input file
file_path = filedialog.askopenfilename(title="Select Input File",
                                       filetypes=[("All Files", "*.*")])

if not file_path:
    print("No file selected. Exiting...")
    exit()

# Read data from the selected file
with open(file_path, 'r') as file:
    data = file.readlines()

# Extracting individual IDs, populations, and proportions
individuals = []
populations = []
proportions = []
for row in data:
    parts = row.split()
    individuals.append(parts[0])
    populations.append(int(parts[1]))
    proportions.append([float(part) for part in parts[2:]])

# Calculate the maximum proportion for each individual
max_proportions = [max(proportion) for proportion in proportions]

# Combine individuals, populations, proportions, and max_proportions into a list of tuples
combined_data = list(zip(individuals, populations, proportions, max_proportions))

# Sort the combined data based on maximum proportion (descending) within each population
sorted_data = sorted(combined_data, key=lambda x: (x[1], -x[3]))  # Sort by population and max proportion

# Extract sorted individuals, populations, and proportions
sorted_individuals = [item[0] for item in sorted_data]
sorted_populations = [item[1] for item in sorted_data]
sorted_proportions = [item[2] for item in sorted_data]

# Transpose proportions for plotting
proportions_transposed = list(zip(*sorted_proportions))

# Plotting stacked bar plots
colors = ['blue', 'green', 'red', 'purple', 'orange']  # Colors for clusters
x_positions = range(len(sorted_individuals))
bottom = [0] * len(sorted_individuals)

plt.figure(figsize=(10, 4))  # Adjust figure size, specifically height

for i, cluster_data in enumerate(proportions_transposed):
    plt.bar(x_positions, cluster_data, bottom=bottom, color=colors[i], label=f'Cluster {i+1}')
    bottom = [sum(x) for x in zip(bottom, cluster_data)]

plt.xlabel('Individuals')
plt.ylabel('')
plt.title('')
plt.xticks(x_positions, sorted_individuals, rotation=90, ha='center', fontsize=8)  # Rotate labels, center alignment, and set font size

# Set x-axis limits to remove white space on the left
plt.xlim(-0.5, len(sorted_individuals) - 0.5)

# Add vertical grid lines between populations
for i in range(len(sorted_individuals) - 1):
    if sorted_populations[i] != sorted_populations[i + 1]:
        plt.axvline(x=i + 0.5, ymin=0, ymax=1, color='black', linewidth=1.5)  # Set ymin=0 and ymax=1 for the line to be within the plot area

# Set y-axis limits to move the top lines down to 1.0
plt.ylim(0, 1.0)

plt.tight_layout()  # Automatically adjusts subplot parameters to give specified padding
plt.show()
