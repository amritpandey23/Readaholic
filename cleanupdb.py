from book_review import db, bcrypt
from book_review.models import Admin

def clean_up():
  db.drop_all()
  db.create_all()
  admin = Admin(email="admin@br.com", password=bcrypt.generate_password_hash("123456").decode("utf-8"))
  db.session.add(admin)
  db.session.commit()