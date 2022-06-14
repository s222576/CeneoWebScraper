from app import app
from flask import render_template

@app.route('/')
@app.route('/index')

def index():
    name = 'Bondarenko Vladyslav'
    return render_template('index.html.jinja', name=name)


@app.route('author')
@app.route('/templates/author')

def author():
    index_number = '222576'
    field_of_study = 'Applied informatics'
    return render_template('author.html.jinja', index_number=index_number, field_of_study=field_of_study)
    def products():
        return render_template