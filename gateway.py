from flask import Flask, Blueprint, render_template, request, redirect, session, send_file
from main_functions import *
from document_edit_functions import *

docu_flow_app = Flask(__name__)
docu_flow_blueprint = Blueprint('docu_flow', __name__)

docu_flow_app.config.from_object('config.Config')
docu_flow_config = docu_flow_app.config

create_folder('documents')

@docu_flow_blueprint.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@docu_flow_blueprint.route('/explanation', methods=['GET', 'POST'])
def explanation():
    if request.method == 'POST':
        document = request.files.get('document', '')
        if document=='' or document.filename=='':
            return render_template('explanation.html', warning_title="Документ не вказаний")
        
        document_text = get_document_text(document)
        document_name = get_unique_name("documents", "".join(document.filename.split('.')[:-1]), '.txt')+'.txt'
        print(document_name)
        save_text_file(document_name, document_text)

        return redirect(f'/constructor/{document_name}')

    return render_template('explanation.html')



@docu_flow_blueprint.route('/creation', methods=['GET', 'POST'])
def creation():
    if request.method == 'POST':
        user_request = request.form['request']
        if len(user_request)<30:
            return render_template('creation.html', warning_title="Запит дуже короткий", user_request=user_request)
        
        document_text = create_document(user_request)
        document_name = get_unique_name("documents", 'document', '.txt') + '.txt'
        save_text_file(document_name, document_text)

        return redirect(f'/constructor/{document_name}')

    return render_template('creation.html')



@docu_flow_blueprint.route('/constructor/<string:document_name>', methods=['GET'])
def constructor(document_name):
    document_text = get_text_from_document(f'documents/{document_name}')
    return render_template('constructor.html', document_name=document_name, document_text=document_text)


@docu_flow_blueprint.route('/explain_constructor/<string:document_name>', methods=['GET', 'POST'])
def explain_constructor(document_name):
    explain_part=''
    explain_result=''
    if request.method == 'POST':
        document_text = request.form['text']
        save_text_file(document_name, document_text)

        explain_part = request.form['part'].replace("\n", "<br>")
        explain_result = explain_part_function(explain_part, document_name).replace("\n", "<br>")

    explain_document = explain_full_document(document_name).replace("\n", "<br>")

    return render_template('constructor_explained.html', explain_part=explain_part, document_name=document_name, explain_result=explain_result, explain_document=explain_document)



docu_flow_app.register_blueprint(docu_flow_blueprint)

docu_flow_app.run(port=8080)