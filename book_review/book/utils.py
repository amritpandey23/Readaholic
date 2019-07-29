import os, uuid
from book_review import app
from werkzeug.utils import secure_filename

def save_cover_image(cover_image):
  f = cover_image.data
  filename = f"{str(uuid.uuid4())}.{f.filename.rsplit('.', 1)[1].lower()}"
  f.save(os.path.join(app.instance_path, "uploads", filename))
  return filename

def delete_cover_image(filename):
  os.remove(os.path.join(app.instance_path, "uploads", filename))