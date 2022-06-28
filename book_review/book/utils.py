import os
from uuid import uuid4
from book_review import app
from werkzeug.utils import secure_filename

def save_cover_image(cover_image):
  f = cover_image.data
  filename = f"picture-{str(uuid4())}.{f.filename.split('.')[1].lower()}"
  f.save(os.path.join(app.instance_path, "uploads", filename))
  return filename

def delete_cover_image(filename):
  os.remove(os.path.join(app.instance_path, "uploads", filename))