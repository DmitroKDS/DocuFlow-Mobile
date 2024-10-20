import os 



def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_unique_name(folder, name, extension):
    counter, unique_name = 1, name
    
    while os.path.exists(f'{folder}/{unique_name}{extension}'):
        unique_name = f"{name}_{counter}"
        counter += 1
    
    return unique_name


def save_text_file(document_name, document_text):
    with open(f'documents/{document_name}', 'w', encoding='utf-8') as file:
        file.write(document_text)