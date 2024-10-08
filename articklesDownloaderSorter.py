import shutil
import wikipediaapi
import re
import nltk
from collections import Counter
import os
from collections import defaultdict

def delete_all_files_in_directory(directory):
    """
    Deletes all files in the specified directory.
    
    Args:
    directory (str): Path to the directory where files will be deleted.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                # If there are subdirectories, this will delete them too (optional)
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def get_wikipedia_article(title, lang):
    """
    Fetch a Wikipedia article by its title and language.
    
    Args:
    title (str): Title of the Wikipedia article.
    lang (str): Language of the Wikipedia page (e.g., 'en' for English, 'de' for German).
    
    Returns:
    str: Content of the Wikipedia article.
    """
    wiki_wiki = wikipediaapi.Wikipedia("MyTestApp olaf.grykalowski@gmail.com", lang)
    
    page = wiki_wiki.page(title)
    
    if page.exists():
        return page.text
    else:
        return None


def get_translated_title(title, source_lang, target_lang):
    """
    Fetch the translated title of a Wikipedia article from the source language to the target language.
    
    Args:
    title (str): Title of the Wikipedia article in the source language.
    source_lang (str): Source language code (e.g., 'en' for English).
    target_lang (str): Target language code (e.g., 'de' for German).
    
    Returns:
    str: Translated title of the Wikipedia article, or the original title if no translation is available.
    """
    # Provide a valid user agent string
    wiki_wiki = wikipediaapi.Wikipedia( "MyTestApp olaf.grykalowski@gmail.com", source_lang)
    page = wiki_wiki.page(title)
    
    if page.exists():
        # Get the page in the target language
        langlinks = page.langlinks
        if target_lang in langlinks:
            return langlinks[target_lang].title
        else:
            print(f"Translation for '{title}' not available in '{target_lang}'. Using the original title.")
            return title
    else:
        print(f"Page '{title}' does not exist in '{source_lang}'.")
        return None




def download_wikipedia_articles(titles, source_lang, target_lang):
    """
    Download a list of Wikipedia articles by their translated titles.
    
    Args:
    titles (list): List of article titles to download in the source language.
    source_lang (str): The language of the provided titles (e.g., 'en').
    target_lang (str): The language in which to download the articles (e.g., 'de').
    
    Returns:
    dict: Dictionary where the key is the translated article title and the value is the article content.
    """
    articles = {}
    for title in titles:
        print(f"Translating title: {title} from '{source_lang}' to '{target_lang}'")
        translated_title = get_translated_title(title, source_lang, target_lang)
        if translated_title:
            print(f"Downloading article: {translated_title} in language '{target_lang}'")
            article_text = get_wikipedia_article(translated_title, target_lang)
            if article_text:
                articles[translated_title] = article_text
                print(f"Article '{translated_title}' downloaded successfully.")
            else:
                print(f"Article '{translated_title}' not found.")
    return articles

def clean_article_text(text):
    """
    Clean the text from Wikipedia articles by removing unwanted characters and formatting issues.
    
    Args:
    text (str): The raw text from the Wikipedia article.
    
    Returns:
    str: Cleaned text.
    """
    # Step 1: Remove unwanted characters (like `/` and `-`)
    cleaned_text = re.sub(r'[\/\-,\.\(\)\'\"\<\>\:\;\?\!\d\“\„\–\%\°c\{\}\[\]\’\…\=\‘\”cs]', '', text)
    
    # Step 2: Replace multiple consecutive newlines with a single newline
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
    
    # Step 3: Remove unnecessary whitespace at the beginning and end of lines
    cleaned_text = re.sub(r'^\s+|\s+$', '', cleaned_text, flags=re.MULTILINE)
    
    # Step 4: Remove multiple spaces if necessary
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)  # Replace multiple spaces with a single space
    
    return cleaned_text




# Download the tokenizer resources from NLTK
nltk.download('punkt')
nltk.download('punkt_tab')

def tokenize_and_count_frequency(text):
    """
    Tokenizes the input text and counts the frequency of each word,
    removing specific unwanted characters (like `/`, `-`), but keeping special characters.
    
    Args:
    text (str): The raw text to tokenize.
    
    Returns:
    Counter: A counter object with word frequencies.
    """
    # Tokenize the text into words
    tokens = nltk.word_tokenize(text.lower())  # Convert to lowercase to normalize words
    
    # Remove specific unwanted characters but keep Unicode letters (including special characters like ś, ö, etc.)
    cleaned_tokens = [re.sub(r'[/-]', '', token) for token in tokens if re.sub(r'[/-]', '', token)]
    
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
    Saves the Zipf's law check results to a file with aligned columns.
    
    Args:
    zipf_results (list): A list of tuples with word, rank, frequency, and rank * frequency product.
    output_file (str): The path of the output file where results will be saved.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header with fixed-width columns
        f.write(f"{'Word':<30}{'Rank':<15}{'Frequency':<15}{'Rank*Frequency':<20}\n")
        f.write("-"*80 + "\n")
        for word, rank, frequency, zipf_product in zipf_results:
            # Format each row with fixed-width columns
            f.write(f"{word:<30}{rank:<15}{frequency:<15}{zipf_product:<20}\n")


'''
Counts each word
Cretes neighbours for each word
'''
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
    "Impressionism",
    "Evolution",
    "Law of Supply and Demand",
    "Stoicism",
    "Socialization",
    "Romanticism in Literature",
    "Quantum Mechanics",
    "Renaissance Art",
    "Black Hole",
    "Microbiology",
    "Photosynthesis",
    "Ancient Egypt",
    "Feminism",
    "Plate Tectonics",
    "Machine Learning",
    "Theory of Relativity",
    "Neanderthals",
    "Ocean Currents",
    "Philosophy of Mind",
    "Artificial Neural Networks",
    "The Cold War",
    "Cryptography",
    "Genetic Engineering",
    "Dark Matter",
    "Classical Music",
    "Roman Empire",
    "Renewable Energy",
    "History of Mathematics",
    "Global Warming",
    "Social Media",
    "Blockchain",
    "Indian Independence Movement",
    "Game Theory",
    "French Revolution",
    "Anthropology",
    "Internet Privacy",
    "Existentialism",
    "Thermodynamics",
    "Civil Rights Movement",
    "General Relativity",
    "Cognitive Dissonance",
    "History of Computing",
    "Gothic Architecture",
    "Epigenetics",
    "Relativity",
    "Middle Ages",
    "Multiverse Theory",
    "Genetic Mutation",
    "Political Philosophy",
    "The Industrial Revolution",
    "Alchemy",
    "Artificial General Intelligence",
    "Cybersecurity",
    "History of Physics",
    "Pandemics",
    "Botany",
    "Viking Age",
    "DNA Sequencing",
    "Feminist Philosophy",
    "History of Medicine",
    "Classical Mythology",
    "Cosmology",
    "History of the United States",
    "Electromagnetic Spectrum",
    "Probability Theory",
    "Urbanization",
    "Information Theory",
    "Robotics",
    "Middle Eastern History",
    "Surrealism",
    "Buddhism",
    "Invasive Species",
    "Chemical Bonding",
    "Ancient Rome",
    "Agricultural Revolution",
    "Evolutionary Psychology",
    "Cybernetics",
    "Space Exploration",
    "String Theory",
    "Solar Energy",
    "Philosophy of Science",
    "Comparative Religion",
    "Environmental Ethics",
    "The Renaissance",
    "Greenhouse Effect",
    "Artificial Satellites",
    "The Great Depression",
    "Epidemiology",
    "Human Genome Project",
    "Medieval Philosophy",
    "Climate Policy",
    "Quantum Computing",
    "Renaissance Literature",
    "Wildlife Conservation",
    "The Scientific Method",
    "The Ottoman Empire",
    "Neolithic Revolution",
    "Psychology of Personality",
    "International Relations",
    "Marxism",
    "Theory of Computation",
    "Nanotechnology",
    "The Human Brain",
    "History of Art",
    "Molecular Biology",
    "The Silk Road"
]


    #Directory where articles will be saved
    article_directory = "./downloaded_articles"

   # Source and target languages
    source_lang = "en"  # e.g., 'en' for English
    target_lang = input("Enter target language code (e.g., 'de' for German): ").strip()

    # Create the directory to store downloaded articles
    create_directory(article_directory)

    # Delete all files in the downloaded_articles directory
    delete_all_files_in_directory(article_directory)

    # Download articles in the specified language
    downloaded_articles = download_wikipedia_articles(article_titles, source_lang, target_lang)

    # Save the articles with translated titles in the filename
    for title, content in downloaded_articles.items():
        file_name = os.path.join(article_directory, f"{title.replace(' ', '_')}_{target_lang}.txt")
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(clean_article_text(content))
    print(f"All cleaned articles saved to '{article_directory}'")


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

    input_file = "aggregated_word_frequencies.txt"
    word_frequencies = load_word_frequencies_from_file(input_file)

    # Rank the words by frequency and calculate the Zipf product
    zipf_results = rank_words_by_frequency(word_frequencies)

    # Save the Zipf's law results to a file
    output_file = "zipf_law_results.txt"
    save_zipf_results(zipf_results, output_file)
    print(f"Zipf's law results saved to '{output_file}'")



