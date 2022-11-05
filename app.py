#!/bin/python3
import flask, flask_login
import random, string
from datetime import datetime
from base import app,load_info,ajax,DBDict

# -- Info for every Hack-A-Day project --
load_info({
    "project_name": "Hack-A-Paste",
    "source_url": "https://github.com/za3k/day05_paste",
    "subdir": "/hackaday/paste"
})

# -- Routes specific to this Hack-A-Day project --
pastes = DBDict("paste")
def random_id():
    LETTERS=string.ascii_letters + string.digits
    return "".join(random.choice(LETTERS) for letter in range(16))

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/create", methods=["POST"])
def create():
    content = flask.request.form.get('text', '')
    if content == '':
        return flask.redirect(flask.url_for("index"))
    key = random_id()
    title = flask.request.form.get('title', '')
    if title == "":
        title = "untitled " + key
    if flask_login.current_user.is_authenticated:
        author = flask_login.current_user.id
    else:
        author = "anonymous"
    paste = {
        "id": key,
        "title": title,
        "content": content,
        "author": author or "guest",
        "creation_time": datetime.now(),
    }
    pastes[key] = paste
    return flask.redirect(flask.url_for("view", paste_id=key))

@app.route("/p/<paste_id>")
def view(paste_id):
    return flask.render_template('view.html', paste=pastes[paste_id])

@app.route("/p/raw/<paste_id>")
def view_raw(paste_id):
    content = pastes[paste_id]["content"]
    return flask.Response(content, mimetype="text/plain")
