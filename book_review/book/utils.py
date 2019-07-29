import os
from book_review import app
from werkzeug.utils import secure_filename

def save_cover_image(cover_image):
  f = cover_image.data
  filename = secure_filename(f.filename)
  f.save(os.path.join(app.instance_path, "uploads", filename))
  return filename