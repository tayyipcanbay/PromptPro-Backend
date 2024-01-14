from flask import Flask, request
from werkzeug.utils import secure_filename
from tesseract_operations import tesseract_it
from database_operations import (
    create_user_if_not_exists,
)
from gpt_request import run_query
import os
import json
import uuid

app = Flask(__name__)


def save_image(request):
    image = request.files['image']
    image_name = str(uuid.uuid4()) + ".jpg"
    image_dir = "images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    image_path = os.path.join(image_dir, image_name)
    image.save(image_path)
    return image_path

@app.route("/")
def index():
    return "Hello World"

UPLOAD_FOLDER = 'images'

@app.route("/ask-image", methods=["POST"])
def ask_image():
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            return json.dumps({"status":400, "error": "No file part"})
        file = request.files['file']
        email = request.form.get('email')
        token = request.form.get('token')
        text = request.form.get('text')
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return json.dumps({"status":400, "error": "No selected file"})
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_text = tesseract_it(image_path)
            print(f"Received text: {image_text}")
            prompt = f"""
            This is my question body.\n
            #start\n
            {image_text}\n
            #end\n
            {text}
            """
            print(prompt)
            response = run_query(token, prompt)
            return json.dumps({"status":200, "text": response})
    else:
        return json.dumps({"status":400, "error": "Invalid request method"})
        

@app.route("/ask-text", methods=["POST"])
def ask_text():
    if request.method == "POST":
        text = request.json["text"]
        token = request.json["token"]
        email = request.json["email"]
        print(f"Received text: {text}")
        response = run_query(token, text)
        return json.dumps({"status":200, "text": response})
    else:
        return json.dumps({"status":400})

@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    token = request.json["token"]   
    if request.method == "POST":
        user_id = create_user_if_not_exists(token, email)
        return json.dumps({"user_id": user_id, "status":200})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3131, debug=True)
