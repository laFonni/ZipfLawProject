
def load_zipf_results(file_path):
    """
    Loads the Zipf's law results from a file and returns a list of tuples (word, frequency).
    
    Args:
    file_path (str): The path of the file containing Zipf's law results.
    
    Returns:
    list: A list of tuples with word and frequency.
    """
    zipf_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip the header
        next(f)  # Skip the separator line

        for line in f:
            # Ensure the line is not empty
            if line.strip():
                # Split by spaces but remove extra spaces between columns
                parts = line.strip().split()
                if len(parts) >= 3:
                    word = parts[0]
                    frequency = int(parts[2])  # Frequency is in the third position
                    zipf_data.append((word, frequency))
    
    return zipf_data


def detect_hapax_legomena(zipf_data):
    """
    Detects hapax legomena (words that occur only once).
    
    Args:
    zipf_data (list): A list of tuples containing word and frequency.
    
    Returns:
    list: A list of words that occur only once.
    """
    return [word for word, frequency in zipf_data if frequency == 1]

def compute_text_coverage(zipf_data, percentage):
    """
    Computes the percentage of text that can be understood by knowing a certain percentage of the most frequent words.
    
    Args:
    zipf_data (list): A list of tuples containing word and frequency.
    percentage (float): The percentage of the most frequent words to consider.
    
    Returns:
    float: The percentage of the total text covered by the most frequent words.
    """
    total_word_count = sum(frequency for _, frequency in zipf_data)
    words_to_consider = int(len(zipf_data) * (percentage / 100))
    
    # Sum the frequencies of the most frequent words
    top_words_count = sum(frequency for _, frequency in zipf_data[:words_to_consider])
    
    # Calculate the percentage of the text covered by these words
    coverage = (top_words_count / total_word_count) * 100
    
    return coverage

def save_hapax_legomena(hapax_legomena, output_file):
    """
    Saves hapax legomena to a file.
    
    Args:
    hapax_legomena (list): A list of hapax legomena.
    output_file (str): The path of the output file where results will be saved.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in hapax_legomena:
            f.write(f"{word}\n")

def save_text_coverage_words(zipf_data, output_file, percentages=[10, 20, 30, 40, 50]):
    """
    Saves words grouped by the percentage of total word occurrences they cover.
    
    Args:
    zipf_data (list): A list of tuples containing word and frequency.
    output_file (str): The path of the output file where results will be saved.
    percentages (list): List of percentage thresholds to group words.
    """
    total_word_count = sum(frequency for _, frequency in zipf_data)  # Total occurrences of words
    cumulative_word_count = 0
    current_percentage_idx = 0
    words_by_percentage = {p: [] for p in percentages}  # Dictionary to hold words by percentage sections
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (word, frequency) in enumerate(zipf_data):
            cumulative_word_count += frequency
            current_coverage = (cumulative_word_count / total_word_count) * 100

            # Calculate the percentage each word covers
            word_coverage = (frequency / total_word_count) * 100
            word_with_coverage = f"{word} ({word_coverage:.2f}%)"
            
            # Add the current word to the current percentage group
            if current_percentage_idx < len(percentages):
                words_by_percentage[percentages[current_percentage_idx]].append(word_with_coverage)

            # Move to the next percentage threshold when the coverage exceeds the current threshold
            while current_percentage_idx < len(percentages) and current_coverage >= percentages[current_percentage_idx]:
                current_percentage = percentages[current_percentage_idx]
                f.write(f"\nWords covering {current_percentage}% of the text:\n")
                f.write(", ".join(words_by_percentage[current_percentage]) + "\n")
                current_percentage_idx += 1

        # In case there are leftover words to write for the last group
        while current_percentage_idx < len(percentages):
            current_percentage = percentages[current_percentage_idx]
            f.write(f"\nWords covering {current_percentage}% of the text:\n")
            f.write(", ".join(words_by_percentage[current_percentage]) + "\n")
            current_percentage_idx += 1

def save_words_in_coverage_range(zipf_data, output_file, start_percentage, end_percentage):
    """
    Saves words to a file whose cumulative frequency coverage overlaps with the given percentage range.

    Args:
    zipf_data (list): A list of tuples containing word and frequency.
    output_file (str): The path of the output file where results will be saved.
    start_percentage (float): The starting percentage of cumulative coverage.
    end_percentage (float): The ending percentage of cumulative coverage.
    """
    total_word_count = sum(frequency for _, frequency in zipf_data)
    cumulative_word_count = 0
    words_in_range = []

    for word, frequency in zipf_data:
        previous_cumulative_coverage = (cumulative_word_count / total_word_count) * 100
        cumulative_word_count += frequency
        cumulative_coverage = (cumulative_word_count / total_word_count) * 100

        # Check if the coverage range of the current word overlaps with the desired range
        if cumulative_coverage >= start_percentage and previous_cumulative_coverage <= end_percentage:
            words_in_range.append(word)
        if cumulative_coverage > end_percentage:
            break  # Exit the loop if we've exceeded the end percentage

    with open(output_file, 'w', encoding='utf-8') as f:
        for word in words_in_range:
            f.write(f"{word}\n")

def filter_word_neighbors(words_of_interest_file, word_neighbors_file, output_file):
    """
    Filters word neighbors based on a list of words of interest and saves the result to an output file.
    
    Args:
    words_of_interest_file (str): Path to the file containing words of interest.
    word_neighbors_file (str): Path to the file containing word neighbors.
    output_file (str): Path to the output file to save filtered word neighbors.
    """
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
            
            # Ensure that if the filtered_neighbors list has entries, the first one is not removed
            if filtered_neighbors:
                word_neighbors_list.append((word, filtered_neighbors))
            else:
                # Even if no neighbors are left, still append the word with an empty list
                word_neighbors_list.append((word, []))

    # Step 3: Sort the words by the number of neighbors (from most to least)
    word_neighbors_list.sort(key=lambda x: len(x[1]), reverse=True)

    # Step 4: Write the sorted words and their neighbors to the output file
    with open(output_file, 'w') as fout:
        for word, filtered_neighbors in word_neighbors_list:
            if filtered_neighbors:
                fout.write(f"{word}: {', '.join(filtered_neighbors)}\n")
            else:
                fout.write(f"{word}:\n")


def exportData(rangeOfWords):
    
    if not isinstance(rangeOfWords, int):
        raise TypeError(f"The 'range' argument must be an integer, but got {type(range).__name__}")

    # Load the Zipf's law results from the file
    zipf_file = "zipf_law_results.txt"
    zipf_data = load_zipf_results(zipf_file)
    
    # Detect hapax legomena
    hapax_legomena = detect_hapax_legomena(zipf_data)
    
    # Save hapax legomena to a file
    hapax_output_file = "hapax_legomena.txt"
    save_hapax_legomena(hapax_legomena, hapax_output_file)
    print(f"Hapax legomena saved to '{hapax_output_file}'")
    
    # Save words grouped by percentage coverage based on total word occurrences
    coverage_output_file = "text_coverage_by_percentage.txt"
    save_text_coverage_words(zipf_data, coverage_output_file)
    print(f"Text coverage words saved to '{coverage_output_file}'")

    # Save words within the coverage range
    range_output_file = "words_in_range.txt"
    save_words_in_coverage_range(zipf_data, range_output_file, 0, rangeOfWords)
    print(f"Words in coverage range saved to '{range_output_file}'")

    # Filter word neighbors based on the words of interest
    words_of_interest_file = 'words_in_range.txt'  # Second file 
    word_neighbors_file = 'word_neighbors.txt'            # First file
    output_file = 'filtered_word_neighbors.txt'           # Output file

    filter_word_neighbors(words_of_interest_file, word_neighbors_file, output_file)
    print(f"Filtered word neighbors saved to '{output_file}'")

# def test():
    #