from django.shortcuts import render
import dominate
import json
from dominate.tags import *
import string
import os.path
import datetime
#from git import Repo
# Create your views here.


def home(request):
    return render(request, "index.html")

# def result(request):
#     return render(request, 'result.html')

def process(request):
    config = json.loads(request.POST["JSONInput"])
    doc = dominate.document(title="Ordered Page")
    with doc.head:
        style("""\
            body {
                background-color: #add8e6;
                color: #2C232A;
                font-family: sans-serif;
                margin: 100px 300px;
                font-size: 16px;
            }
            input[type=text], select, textarea, input[type=file], input[type=password], input[type=date], input[type=email], input[type=range], input[type=number] {
                width: 100%;
                padding: 12px 0 12px 0px;
                border: 1px solid #ccc;
                text-indent:12px;
                border-radius: 4px;
                resize: none;
                
            }

            textarea {
                width: 100%;
                padding: 12px 0 12px 0px;
                border: 1px solid #252525;
                text-indent:12px;
                border-radius: 4px;
                resize: vertical;
            }
            
            div {
                padding: 10px 0 10px 0;
            }

            label {
                padding: 12px 12px 12px 0;
                display: inline-block;
            }

            input[type=submit] {
                background-color: #000080;
                color: white;
                padding: 12px 20px;
                margin: 30px 0 30px 0;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            }

            input[type=submit]:hover {
                background-color: #002c40;
            }

        """)

        html = form(action="/", method="GET")
        with html:
            h1('Ordered Form')
            for input_config in config['Attributes']:

                if input_config['Type'] == 'select':

                    generate_select_input(input_config)

                elif input_config['Type'] == 'textarea':

                    generate_textarea_input(input_config)

                elif input_config['Type'] == 'radio' or input_config['Type'] == 'checkbox':

                    generate_radio_input(input_config)

                elif input_config['Type'] == 'date':
                    generate_date_input(input_config)

                elif input_config['Type'] == 'number' or input_config['Type'] == 'range':
                    generate_number_input(input_config)

                elif input_config['Type'] == 'file':
                    generate_file_input(input_config)

                else:
                    generate_text_input(input_config)
            input_(_class='button', type='submit',
                   value=config['ActionDisplay'])
    generate_file(doc)

    return render(request, "result.html", {"result": doc.render()})


def generate_file(doc):
    dir1 = os.path.join(os.getcwd(), 'GeneratedFile')
    date = datetime.datetime.now()
    now = date.strftime("%Y-%m-%d %H-%M-%S")
    dirPath2 = os.path.join(dir1, 'Genarated_Page_')
    dirPath = dirPath2.rstrip('\n')
    filenameCreated = dirPath+now
    a_file = open(filenameCreated + ".html", "w")
    print(doc.render(), file=a_file)
    a_file.close()

    # Git Push
 #   repo = Repo('./GeneratedFile')
  #  repo.index.add([filenameCreated + ".html"])
   # repo.index.commit('Generated File Push'+now)
    #origin = repo.remote('origin')
    #origin.push()


def generate_text_input(input):
    html = div()
    with html:
        label(input['Name'])
        input_(
            type=input['Type'],
            maxlength=input['Size'] if 'Size' in input else '',)
    return html


def generate_file_input(input):
    html = div()
    with html:
        label(input['Name'])
        input_(
            type=input['Type'])
    return html


def generate_date_input(input):
    html = div()
    with html:
        label(input['Name'])
        input_(
            type=input['Type'],
            max=input['Maximum'] if 'Maximum' in input else '',
            min=input['Minimum'] if 'Minimum' in input else '')
    return html


def generate_number_input(input):
    html = div()
    with html:
        label(input['Name'])
        input_(
            type=input['Type'],
            max=input['Maximum'] if 'Maximum' in input else '',
            min=input['Minimum'] if 'Minimum' in input else '',
            step=input['Step'] if 'Step' in input else '')
    return html


def generate_textarea_input(input):
    html = div()
    with html:
        label(input['Name'])
        textarea(rows=input['RowSize'] if 'RowSize' in input else '20',
                 cols=input['ColSize'] if 'ColSize' in input else '60')

    return html


def generate_select_input(input):
    html = div()
    with html:
        label(input['Name'])
        dropdown = select()
        with dropdown:
            for dropdown_options in input['DropdownValues']:
                option(dropdown_options['DisplayValue'],
                       value=dropdown_options['Value'])

    return html


def generate_radio_input(input):
    html = div()
    with html:
        label(input['Name'])
        for radio_options in input['Options']:
            radiobutton = input_(type=input['Type'],
                                 value=radio_options['Value'],
                                 name=input['Name'])
            label(radio_options['DisplayValue'])

    return html
