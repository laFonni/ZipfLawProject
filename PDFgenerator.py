

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def generate_PDF():
    # Reading data from the zipf_law_results.txt file
    zipf_law_file_path = "zipf_law_results.txt"
    with open(zipf_law_file_path, "r", encoding="utf-8") as file:
        zipf_law_data = file.readlines()

    # Load the text_coverage_by_percentage.txt content
    text_coverage_file_path = "text_coverage_by_percentage.txt"
    with open(text_coverage_file_path, "r") as file:
        text_coverage_data = file.readlines()

    # Extracting relevant columns (Word, Rank, Frequency, Rank*Frequency)
    table_data = [["Word", "Rank", "Frequency", "Rank*Frequency"]]  # Table header
    for line in zipf_law_data[2:22]:  # Let's take the first 10 words as an example
        parts = line.split()
        word = parts[0]
        rank = parts[1]
        frequency = parts[2]
        rank_frequency = parts[3]
        table_data.append([word, rank, frequency, rank_frequency])

    # Create a new PDF file
    pdf_file_path = "zipf_law_results_table_spaced.pdf"
    pdf = SimpleDocTemplate(pdf_file_path, pagesize=letter)

    # Use styles for titles and text, specifying the Times-Roman font
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Times-Roman", fontName="Times-Roman", fontSize=12))

    # Title and other text sections using Times-Roman
    title = Paragraph("Zipf's Law Analysis Report", styles['Title'])
    word_info_title = Paragraph("Word Frequency Information:", styles['Times-Roman'])

    # Extracting text coverage info
    coverage_10_percent = text_coverage_data[2].strip()
    coverage_20_percent = text_coverage_data[5].strip()
    coverage_30_percent = text_coverage_data[8].strip()

    # Custom paragraph style for the text coverage section with more spacing between lines
    coverage_style = ParagraphStyle(
        name="TextCoverage", fontName="Times-Roman", fontSize=12, leading=16
    )
    coverage_style_title = ParagraphStyle(
        name="TextCoverage", fontName="Times-Roman", fontSize=14, leading=16
    )

    # Paragraphs for text coverage data with increased line spacing
    coverage_info_title = Paragraph("Text Coverage Information:", coverage_style_title)
    coverage_text_10_t = Paragraph("Words covering 10% of the text:", coverage_style_title)
    coverage_text_10 = Paragraph(f"{coverage_10_percent}", coverage_style)

    coverage_text_20_t = Paragraph("Words covering 20% of the text:", coverage_style_title)
    coverage_text_20 = Paragraph(f"{coverage_20_percent}", coverage_style)

    coverage_text_30_t = Paragraph("Words covering 30% of the text:", coverage_style_title)
    coverage_text_30 = Paragraph(f"{coverage_30_percent}", coverage_style)
    # Create a table with the extracted data
    table = Table(table_data)

    # Adding some styling to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align text
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),  # Use Times-Roman for the table
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Table grid
    ])

    # Apply the style to the table
    table.setStyle(style)

    # Add the graph image
    image_path = "word_neighbors_graph.png"
    img = Image(image_path)
    img.drawHeight = 3 * inch
    img.drawWidth = 3 * inch

    # Build the PDF with the title, table, and image, adding spaces between elements
    elements = [
        title, Spacer(1, 0.2 * inch),
        word_info_title, Spacer(1, 0.2 * inch),
        table, Spacer(1, 0.4 * inch),
        coverage_info_title, Spacer(1, 0.2 * inch),
        coverage_text_10_t,Spacer(1, 0.05 * inch),
        coverage_text_10, Spacer(1, 0.1 * inch),
        coverage_text_20_t,Spacer(1, 0.05 * inch),
        coverage_text_20, Spacer(1, 0.1 * inch),
        coverage_text_30_t,Spacer(1, 0.05 * inch),
        coverage_text_30, Spacer(1, 0.4 * inch),
        img
    ]

    pdf.build(elements)

    print(f"PDF generated: {pdf_file_path}")