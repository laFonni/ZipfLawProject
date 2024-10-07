import wikipediaapi
import re
import nltk
from collections import Counter
import os
from collections import defaultdict

def load_word_frequencies_from_file(file_path):
    """
    Loads word frequencies from a file and returns a Counter object.
    
    Args:
    file_path (str): The path of the file containing word frequencies.
    
    Returns:
    Counter: A counter object with word frequencies.
    """
    word_frequencies = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            word, count = line.strip().split(": ")
            word_frequencies[word] = int(count)
    
    return word_frequencies

def rank_words_by_frequency(frequencies):
    """
    Rank the words by their frequency and calculate the product of rank and frequency.
    
    Args:
    frequencies (Counter): A counter object containing word frequencies.
    
    Returns:
    list: A list of tuples containing word, rank, frequency, and the product of rank and frequency.
    """
    # Sort the words by frequency in descending order
    ranked_words = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    
    # Create a list to store the results: word, rank, frequency, and rank * frequency product
    zipf_results = []
    
    for rank, (word, frequency) in enumerate(ranked_words, 1):  # Start ranking from 1
        zipf_product = rank * frequency
        zipf_results.append((word, rank, frequency, zipf_product))
    
    return zipf_results

def save_zipf_results(zipf_results, output_file):
    """
    Saves the Zipf's law check results to a file.
    
    Args:
    zipf_results (list): A list of tuples with word, rank, frequency, and rank * frequency product.
    output_file (str): The path of the output file where results will be saved.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Word\t\tRank\t\t\tFrequency\t\t\tRank*Frequency\n")
        for word, rank, frequency, zipf_product in zipf_results:
            f.write(f"{word}\t\t\t{rank}\t\t\t\t{frequency}\t\t\t\t{zipf_product}\n")

if __name__ == "__main__":
    # Load the aggregated word frequencies from the file
    input_file = "aggregated_word_frequencies.txt"
    word_frequencies = load_word_frequencies_from_file(input_file)

    # Rank the words by frequency and calculate the Zipf product
    zipf_results = rank_words_by_frequency(word_frequencies)

    # Save the Zipf's law results to a file
    output_file = "zipf_law_results.txt"
    save_zipf_results(zipf_results, output_file)
    print(f"Zipf's law results saved to '{output_file}'")
