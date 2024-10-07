# Define the file paths
# Define the file paths
words_of_interest_file = 'words_in_10_to_50_percent_range.txt'      # Second file
word_neighbors_file = 'word_neighbors.txt'            # First file
output_file = 'filtered_word_neighbors.txt'           # Output file

# Step 1: Read the list of words of interest into a set
with open(words_of_interest_file, 'r') as f:
    words_of_interest = set(line.strip() for line in f if line.strip())

# Step 2: Collect words and their filtered neighbors
word_neighbors_list = []  # List to store tuples of (word, filtered_neighbors)

with open(word_neighbors_file, 'r') as fin:
    for line in fin:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        # Check if the line contains a colon
        if ':' not in line:
            continue  # Skip lines that don't have neighbors
        # Split the line into the word and its neighbors
        word_part, neighbors_part = line.split(':', 1)
        word = word_part.strip()
        # Check if the main word is in the list of interest
        if word not in words_of_interest:
            continue  # Skip words not in the list
        # Split and clean the neighbors
        neighbors = [neighbor.strip() for neighbor in neighbors_part.split(',')]
        # Filter neighbors to include only those in the list, excluding the word itself
        filtered_neighbors = [n for n in neighbors if n in words_of_interest and n != word]
        # Add the word and its filtered neighbors to the list
        word_neighbors_list.append((word, filtered_neighbors))

# Step 3: Sort the words by the number of neighbors (from most to least)
word_neighbors_list.sort(key=lambda x: len(x[1]), reverse=True)

# Step 4: Write the sorted words and their neighbors to the output file
with open(output_file, 'w') as fout:
    for word, filtered_neighbors in word_neighbors_list:
        if filtered_neighbors:
            fout.write(f"{word}: {', '.join(filtered_neighbors)}\n")
        else:
            fout.write(f"{word}:\n")
