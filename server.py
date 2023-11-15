from flask import Flask
from flask import request
from flask import redirect
import random

app = Flask(__name__)

nextId = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]

def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
        <li><a href="/update/{id}/">update</a></li>
        <li>
            <form action="/delete/{id}/" method="POST">
                <input type="submit" value="delete">
            </form>
        </li>
        '''
    
    return f'''
    <!doctype html>
    <body>
        <h1><a href="/">WEB</a></h1>
        <ol>
            {contents}
        </ol>
        {content}
        <ul>
            <li><a href="/create">create</a></li>
            {contextUI}
        </ul>
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

    return template(getContents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=["GET", "POST"])
def create():
    
    if request.method == "GET":
        content = '''
        <h2>create</h2>
        <form action="/create/" method="POST">
            <p><input type="text" name="title_field" placeholder="title"></p>
            <p><textarea name="body_field" placeholder="body"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method == "POST":
        global nextId
        title = request.form.get("title_field")
        body = request.form.get("body_field")
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/' + str(nextId)
        nextId = nextId + 1
        return redirect(url)

@app.route('/update/<int:id>/', methods=["GET", "POST"])
def update(id):
    
    if request.method == "GET":
        title, body = '', ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break

        content = f'''
        <h2>update</h2>
        <form action="/update/{id}/" method="POST">
            <p><input type="text" name="title_field" placeholder="title" value={title}></p>
            <p><textarea name="body_field" placeholder="body">{body}</textarea></p>
            <p><input type="submit" value="update"></p>
        </form>
        '''
        return template(getContents(), content)
        
    elif request.method == "POST":
        global nextId
        title = request.form.get("title_field")
        body = request.form.get("body_field")
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break

        url = '/read/' + str(id)

        return redirect(url)


@app.route('/delete/<int:id>/', methods=["POST"])
def delete(id):
    for topic in topics:
        if topic['id'] == id:
            topics.remove(topic)

    return redirect('/')

app.run(port=5001, debug=True)