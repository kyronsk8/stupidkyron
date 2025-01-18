import os
from flask import Flask, redirect, request
from google.cloud import storage

# Configure Google Cloud Storage
BUCKET_NAME = "cnd-storage"  # Replace with your bucket name
PROJECT_ID = "your-project-id"  # Replace with your project ID
storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

app = Flask(__name__)

@app.route('/')
def index():
    index_html = """
    <form method="post" enctype="multipart/form-data" action="/upload" method="post">
        <div>
            <label for="file">Choose file to upload</label>
            <input type="file" id="file" name="form_file" accept="image/jpeg, image/png, image/gif"/>
        </div>
        <div>
            <button>Submit</button>
        </div>
    </form>
    <div>
        <h2>Uploaded Images:</h2>
        <ul>
    """

    try:
        blobs = list(bucket.list_blobs())
        if blobs:
            for blob in blobs:
                public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob.name}"
                index_html += f"<li><a href=\"{public_url}\" target=\"_blank\">{blob.name}</a></li>" # Added target="_blank"
        else:
            index_html += "<p>No Images Uploaded Yet</p>"
    except Exception as e:
        index_html += f"<p>Error: Could not list files from bucket. Check if bucket '{BUCKET_NAME}' exists and permissions are correct. Details: {e}</p>"

    index_html += """
        </ul>
    </div>
    """
    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    if 'form_file' not in request.files:
        return 'No file part'

    file = request.files['form_file']
    if file.filename == '':
        return 'No selected file'

    try:
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return redirect("/")
    except Exception as e:
        return f"An error occurred during upload: {e}"

if __name__ == '__main__':
    app.run(debug=True)