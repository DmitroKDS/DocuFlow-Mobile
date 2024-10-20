import docx
from pypdf import PdfReader
import openai
from config import Config

def get_document_text(document):
    if document.mimetype == "application/pdf":
        document_text =  '\n'.join(pdf_page.extract_text() for pdf_page in PdfReader(document.stream).pages)
    elif document.mimetype == "text/plain":
        document_text = document.read().decode('utf-8')
    elif document.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document = docx.Document(document.stream)
        document_text =  '\n'.join(paragraph.text for paragraph in document.paragraphs)
        
    return document_text
    

def create_document(user_request):
    chat_gpt_request = openai.OpenAI(api_key=Config.CHAT_GPT_TOKEN)

    document_text = chat_gpt_request.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f'create request:{user_request}'},
            {"role": "assistant", "content": f'Your task is to create a detailed and well-formatted document that matches the user’s request. The document must be written in the language of the specified country(Ukraine) use ukrainian laws, and contain over 10000 characters.\n\nFollow these guidelines to ensure the document meets the requirements:\n\nLanguage: Write the document in the language of the specified country.\nFormat & Placeholders: For any data you do not have, use placeholders in the <[data]> format. Make the name of this data clear and relevant to the content.\nLength: Ensure the document contains more than 6000 characters.\nPresentation: Structure and format the document to look aesthetically pleasing and professional. Use headings, subheadings, paragraphs, and bullet points where appropriate'}
        ]
    ).choices[0].message.content

    return document_text

def get_text_from_document(document_path):
    with open(document_path, 'r') as document:
        document_text = document.read()
    
    return document_text

def explain_part_function(explain_part, document_name):
    document_text = get_text_from_document(f'documents/{document_name}')

    chat_gpt_request = openai.OpenAI(api_key=Config.CHAT_GPT_TOKEN)

    explain_result = chat_gpt_request.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f'document:{document_text}'},
            {"role": "system", "content": f'document part:{explain_part}'},
            {"role": "assistant", "content": f'(Country Ukraine).\nYour task is to write a simple and clear explanation of a specific part of a document. The explanation should use very basic words suitable for an ordinary person and should include important details like names, numbers, and other relevant information using placeholders in the <[data]> format.\n\nThe explanation should:\n\nBe written in the language of the specified country.\nUse simple and clear language while including key details.\nBe structured and visually appealing, using headings, bullet points, and paragraphs where appropriate.\n'}
        ]
    ).choices[0].message.content

    return explain_result


def explain_full_document(document_name):
    document_text = get_text_from_document(f'documents/{document_name}')

    chat_gpt_request = openai.OpenAI(api_key=Config.CHAT_GPT_TOKEN)

    explain_result = chat_gpt_request.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f'document:{document_text}'},
            {"role": "assistant", "content": f'(Country Ukraine).\nYour task is to write a detailed and well-structured explanation of a document, simplifying it for an ordinary person while maintaining important details (such as names, numbers, etc.).Make many neter for easy to read.\n\nThe explanation should:\n\nCover the main points of the document in clear and simple language.\nInclude specific details like names, numbers, and other relevant data as placeholders in the <[data]> format.\nBe written in the language of the specified country.\nContain over 1000 characters.\nBe presented in a structured and aesthetically pleasing format, using headings, bullet points, and paragraphs where appropriate.'}
        ]
    ).choices[0].message.content
    return explain_result