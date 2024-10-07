import wikipediaapi
import re
import nltk
from collections import Counter
import os
from collections import defaultdict

def get_wikipedia_article(title, lang='en'):
    """
    Fetch a Wikipedia article by its title.
    
    Args:
    title (str): Title of the Wikipedia article.
    lang (str): Language of the Wikipedia page (default is 'en').
    
    Returns:
    str: Content of the Wikipedia article.
    """
    wiki_wiki = wikipediaapi.Wikipedia('Mytest (olaf.grykalowski@gmail.com)', "en")
    page = wiki_wiki.page(title)
    
    if page.exists():
        return page.text
    else:
        return None

def download_wikipedia_articles(titles, lang='en'):
    """
    Download a list of Wikipedia articles by their titles.
    
    Args:
    titles (list): List of article titles to download.
    lang (str): Language of the Wikipedia page (default is 'en').
    
    Returns:
    dict: Dictionary where the key is the article title and the value is the article content.
    """
    articles = {}
    for title in titles:
        print(f"Downloading article: {title}")
        article_text = get_wikipedia_article(title, lang)
        if article_text:
            articles[title] = article_text
            print(f"Article '{title}' downloaded successfully.")
        else:
            print(f"Article '{title}' not found.")
    return articles

def clean_article_text(text):
    """
    Clean the text from Wikipedia articles by removing unnecessary line breaks and unwanted formatting issues.
    
    Args:
    text (str): The raw text from the Wikipedia article.
    
    Returns:
    str: Cleaned text.
    """
    # Step 1: Remove unwanted line breaks (when there is a break in the middle of a word/sentence)
    # This assumes that any line break followed by a lowercase letter is an unwanted break.
    cleaned_text = re.sub(r'\n([a-z])', r'\1', text)
    
    # Step 2: Remove multiple consecutive newlines and replace them with a single newline
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
    
    # Step 3: Remove any unnecessary whitespace at the beginning and end of lines
    cleaned_text = re.sub(r'^\s+|\s+$', '', cleaned_text, flags=re.MULTILINE)
    
    # Step 4: (Optional) Remove specific known patterns if you notice any other defects in the text
    # For example, you could remove excess spacing or characters like "(token)" shown in the image
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\([a-zA-Z]+\)', '', cleaned_text)  # Remove unwanted "(token)" like words if necessary
    
    return cleaned_text

# Download the tokenizer resources from NLTK
nltk.download('punkt')
nltk.download('punkt_tab')

def tokenize_and_count_frequency(text):
    """
    Tokenizes the input text and counts the frequency of each word,
    removing numbers and punctuation.
    
    Args:
    text (str): The raw text to tokenize.
    
    Returns:
    Counter: A counter object with word frequencies.
    """
    # Tokenize the text into words
    tokens = nltk.word_tokenize(text.lower())  # Convert to lowercase to normalize words
    
    # Remove numbers and punctuation
    cleaned_tokens = [re.sub(r'[^a-zA-Z]', '', token) for token in tokens if re.sub(r'[^a-zA-Z]', '', token)]
    
    # Count the frequency of each token
    word_frequencies = Counter(cleaned_tokens)
    
    return word_frequencies

def create_directory(directory):
    """
    Create a directory if it doesn't exist.
    
    Args:
    directory (str): The path to the directory to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")

def process_articles(directory):
    """
    Process all articles in the specified directory and count word frequencies.
    
    Args:
    directory (str): The path to the directory containing article files.
    
    Returns:
    dict: A dictionary with file names as keys and word frequency counters as values.
    """
    article_frequencies = {}
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                article_text = file.read()
                frequencies = tokenize_and_count_frequency(article_text)
                article_frequencies[filename] = frequencies
                print(f"Processed '{filename}'")
    
    return article_frequencies

def print_word_frequencies(frequencies):
    """
    Prints the word frequencies from the given Counter object.
    
    Args:
    frequencies (Counter): The word frequencies to print.
    """
    for word, count in frequencies.most_common():
        print(f"{word}: {count}")

def save_aggregated_word_frequencies(frequencies, output_file):
    """
    Saves aggregated word frequencies to a file.
    
    Args:
    frequencies (Counter): The word frequencies across all articles.
    output_file (str): The path of the output file where results will be saved.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, count in frequencies.most_common():
            f.write(f"{word}: {count}\n")


def count_word_neighbors(text):
    """
    Counts the immediate neighbors (one on each side) for each word.
    
    Args:
    text (str): The input text to process.
    
    Returns:
    dict: A dictionary where keys are words and values are sets of neighboring words.
    """
    tokens = nltk.word_tokenize(text.lower())  # Tokenize the text into words
    cleaned_tokens = [re.sub(r'[^a-zA-Z]', '', token) for token in tokens if re.sub(r'[^a-zA-Z]', '', token)]
    
    neighbors = defaultdict(set)
    
    for i, word in enumerate(cleaned_tokens):
        if word:  # Ensure the word is not empty
            # Add the left neighbor (if exists)
            if i > 0 and cleaned_tokens[i - 1]:
                neighbors[word].add(cleaned_tokens[i - 1])
            # Add the right neighbor (if exists)
            if i < len(cleaned_tokens) - 1 and cleaned_tokens[i + 1]:
                neighbors[word].add(cleaned_tokens[i + 1])
    
    return neighbors

def save_word_neighbors(neighbors, output_file):
    """
    Saves word neighbors to a file.
    
    Args:
    neighbors (dict): A dictionary where keys are words and values are sets of neighbors.
    output_file (str): The path of the output file where results will be saved.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, neighbor_set in neighbors.items():
            f.write(f"{word}: {', '.join(neighbor_set)}\n")



if __name__ == "__main__":
    # List of 5 different articles you want to download
    article_titles = [
        "Artificial intelligence",
        "World War II",
        "Grand Canyon",
        "DNA",
        "Nelson Mandela",
        "Human Evolution",
        "Democracy",
        "Solar System",
        "Climate Change",
    ]

    #Directory where articles will be saved
    article_directory = "./downloaded_articles"

    # Create the directory to store downloaded articles
    create_directory(article_directory)

    # Download articles
    downloaded_articles = download_wikipedia_articles(article_titles, lang='en')

    # Saving articles to text files
    for title, content in downloaded_articles.items():
        file_name = os.path.join(article_directory, title.replace(" ", "_") + ".txt")
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(clean_article_text(content))
    print(f"Cleaned text saved to '{file_name}'")

     # Path to the directory containing the downloaded Wikipedia article text files
    # Process all articles in the directory
    all_word_frequencies = Counter()

    # Process each article in the directory and aggregate the frequencies
    for filename in os.listdir(article_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(article_directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                article_text = file.read()
                frequencies = tokenize_and_count_frequency(article_text)
                all_word_frequencies.update(frequencies)

    # Save the aggregated frequencies to one file
    output_file = "aggregated_word_frequencies.txt"
    save_aggregated_word_frequencies(all_word_frequencies, output_file)
    print(f"Aggregated word frequencies saved to '{output_file}'")


    # Store neighbors for all articles
    all_word_neighbors = defaultdict(set)

    # Process each article in the directory and collect neighbors
    for filename in os.listdir(article_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(article_directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                article_text = file.read()
                neighbors = count_word_neighbors(article_text)
                for word, neighbor_set in neighbors.items():
                    all_word_neighbors[word].update(neighbor_set)

    # Save the neighbors to a file
    output_file = "word_neighbors.txt"
    save_word_neighbors(all_word_neighbors, output_file)
    print(f"Word neighbors saved to '{output_file}'")



