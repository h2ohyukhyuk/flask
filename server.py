from flask import Flask
import random

app = Flask(__name__)

topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]

def template(contents, content):
    return f'''
    <!doctype html>
    <body>
        <h1><a href="/">WEB</a></h1>
        <ol>
            {contents}
        </ol>
        {content}
    </body>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags += f"<li> <a href='/read/{topic['id']}'> {topic['title']} </a> </li>"
    return liTags


@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>')

@app.route('/read/<int:id>/')
def read(id):
    title, body = '', ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break


    return template(getContents(), f'<h2>{title}</h2>{body}')

app.run(port=5001, debug=True)