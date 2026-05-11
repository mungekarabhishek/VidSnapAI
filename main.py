import os

from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")

        if rec_id:
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            
            for key, value in request.files.items():
                print(key, value)
                file = request.files[key]
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_path, filename))
            
            if desc:
                with open(os.path.join(upload_path, "desc.txt"), "w") as f:
                    f.write(desc)

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

app.run(debug=True)