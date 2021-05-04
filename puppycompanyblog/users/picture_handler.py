import os
from PIL import Image
from puppycompanyblog import app
from flask import url_for,current_app
app_context = app.app_context()
app_context.push()
print(current_app.root_path)
def add_profile_pic(pic_upload,username):
    filename=pic_upload.data.filename
    ext_type=filename.split('.')[-1]
    storage_filename=str(username)+'.'+ext_type
    filepath=os.path.join(current_app.root_path,'static','profile_pics',storage_filename)
    pic = Image.open(pic_upload.data)
    output_size=(200,200)
    pic.thumbnail(output_size)
    pic.save(filepath)
    return storage_filename