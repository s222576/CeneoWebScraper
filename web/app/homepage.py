@app.route('/')
def index():
    name = "Bondarenko Vladyslav"
    return render_template("index.html.jinja", name=name)