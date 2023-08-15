import requests
from bs4 import BeautifulSoup
import json
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def scrape_website(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f'Failed to fetch the URL {url}')

    soup = BeautifulSoup(response.content, 'html.parser')
    headers = soup.find_all(['h1', 'h2', 'h3'])

    documentation = {}
    for header in headers:
        content = []
        sibling = header.find_next(['h1', 'h2', 'h3', 'p'])
        while sibling and sibling.name == 'p':
            content.append(sibling.get_text())
            sibling = sibling.find_next(['h1', 'h2', 'h3', 'p'])
        if content:
            documentation[header.get_text()] = ' '.join(content)

    return documentation


def save_to_json(documentation, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(documentation, json_file, ensure_ascii=False, indent=2)


def save_to_text(documentation, file_name):
    with open(file_name, 'w', encoding='utf-8') as text_file:
        for title, content in documentation.items():
            text_file.write(f'{title}\n')
            text_file.write(f'{content}\n\n')


def save_to_pdf(documentation, file_name):
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    for title, content in documentation.items():
        title_style = ParagraphStyle(name="TitleStyle", fontSize=14, textColor=colors.blue, spaceAfter=12)
        content_style = ParagraphStyle(name="ContentStyle", fontSize=12, textColor=colors.black, spaceAfter=12)

        title_para = Paragraph(title, style=title_style)
        content_para = Paragraph(content, style=content_style)

        elements.append(title_para)
        elements.append(content_para)
        elements.append(Spacer(1, 12))

    doc.build(elements)


if __name__ == '__main__':
    url = 'https://docs.monai.io/en/stable/utils.html'
    try:
        documentation = scrape_website(url)
        save_to_pdf(documentation, 'data/monai_utils.pdf')
        # save_to_text(documentation, 'interview_documentation.txt')
        # save_to_json(documentation, 'documentation.json')
        print('Documentation successfully saved to documentation')
    except Exception as e:
        print(f'Error: {e}')