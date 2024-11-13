from datetime import datetime
from flask import Flask,jsonify, flash, redirect,render_template,request, url_for
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import requests

app=Flask(__name__)

# app.secret_key = 'Secret_Key'

# urls = {
#     'key': '1234',
#     'password': 'password'
# }

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16 MB
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

@app.route('/')
def landing():
    return render_template('index.html')

with app.app_context():
    db.create_all()
 
# Allowed video file extensions
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'avi', 'mov', 'flv'}
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
 
    def __init__(self, filename, path, size):
        self.filename = filename
        self.path = path
        self.size = size
 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/home',methods=['GET'])
def home_page():

    return render_template('home.html')

@app.route('/upload',methods=['GET','POST'])
# @login_required
# def home_page():
#     if(request.method=='POST'):
#         print(request)
#         # url=request.args.get('urml')

#         data=request.get_json()
#         # url=request.form['url']
#         print(data)

#     return render_template('home.html')
def upload_file():
    # Check if the post request has the file part
    if(request.method=='POST'):
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400
    
        file = request.files['file']
    
        # If no file is selected
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
    
        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Secure the filename to avoid path traversal attacks
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            file_size = len(file.read())
    
            # Save the file to the designated folder
            file.seek(0)  # Reset file pointer after reading size
            file.save(filepath)
    
            # Store video metadata in the database
            # new_video = Video(
            #     filename=filename,
            #     path=filepath,
            #     size=file_size
            # )
    
            # # Add to the database session and commit
            # db.session.add(new_video)
            # db.session.commit()

            upload_url = 'https://api.videoindexer.ai/trial/Accounts/c7ae81e6-9046-49b0-8524-cc8a56ed622a/Videos'
            params = {
                'name': 'Video',
                'privacy': 'Private',
                'videoUrl': "C:\\Repository\\Todo\\uploads\\"+filename,
                'isSearchable': 'true',
                'indexingPreset': 'Default',
                'streamingPreset': 'Default',
                'sendSuccessEmail': 'false',
                'useManagedIdentityToDownloadVideo': 'false',
                'preventDuplicates': 'false',
                'accessToken': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJWZXJzaW9uIjoiMi4wLjAuMCIsIktleVZlcnNpb24iOiI3ZmJkMDkxOGRmMWM0NGNjYTI3ZTA2NGQyYWZkYWViOSIsIkFjY291bnRJZCI6ImM3YWU4MWU2LTkwNDYtNDliMC04NTI0LWNjOGE1NmVkNjIyYSIsIkFjY291bnRUeXBlIjoiVHJpYWwiLCJQZXJtaXNzaW9uIjoiQ29udHJpYnV0b3IiLCJFeHRlcm5hbFVzZXJJZCI6IjMxRjc3MEFGRTlGRjRGMEJBRUNDQzU4RjlBOUU3MUU3IiwiVXNlclR5cGUiOiJNaWNyb3NvZnRDb3JwQWFkIiwiSXNzdWVyTG9jYXRpb24iOiJUcmlhbCIsIm5iZiI6MTczMTUwOTEwMiwiZXhwIjoxNzMxNTEzMDAyLCJpc3MiOiJodHRwczovL2FwaS52aWRlb2luZGV4ZXIuYWkvIiwiYXVkIjoiaHR0cHM6Ly9hcGkudmlkZW9pbmRleGVyLmFpLyJ9.I7S90QM7_NkbW2hFPqSYTe7SYCGKX3AMDpkHxTxtfyjuR-a6ab9delUr1HykZpRSGQi0l4FDoLjOR7iySec9H5zag0vXCOECUGv0lE7GdfwZeIRcX-yzMxhhvHiGULj18cM1mzBYKdWFcBR0Dcv5mqti7AlXd6Xb2t9OP-gvn9vEx2oQo5tuKnPIFQWevf6voyDXKs0eMyaa6oH73TfYknwvMBUSDD7fDUy7XtGoW-avMN9RqO53GB0ULTxxIPPAA_-D8BhA86DatOo3uCaIt76q7sag-e7bUJ4vjYm9GrW0U3xaXfSGmQymh3T6XrOG60KwEiUYQ1rni97S74n83Q'
            }
            headers = {
                'Cache-Control': 'no-cache',
                'Ocp-Apim-Subscription-Key': 'e0e1beac58e349b49d50bd0e43bf3cd6'
            }
    
            # Send the POST request
            response = requests.post(upload_url, params=params, headers=headers)
            print(response.json())
    
            # Return success response with video details
            # return jsonify({
            #     'message': 'File uploaded successfully',
            #     'filename': filename,
            #     'path': filepath,
            #     'size': file_size
            # }), 200
            return render_template('home.html',id=response.id)
        else:
            # return jsonify({'message': 'Invalid file type'}), 400
            return render_template('home.html')
    else:
        return render_template('home.html')
 
@app.route('/about')
def about():
    return render_template('about.html')



if __name__=="__main__":
    app.run(debug=True)
