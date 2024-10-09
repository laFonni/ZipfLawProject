from articklesDownloaderSorter import download_and_process_articles
from exporter import exportData
from graphGenerator import generate_graphs
from PDFgenerator import generate_PDF

def main():
    # Call the functions from each file in the order you need
    download_and_process_articles() # Function from articklesDownloader.py
    exportData(20)    # Function from exportOfResults.py args - range of intersted words (int)
    generate_graphs()    # Function from graphGenerator.py
    generate_PDF()

if __name__ == "__main__":
    main()
