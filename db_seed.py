from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models import db, User


with app.app_context():
  db.drop_all()
  db.create_all()

  user = User(user_name="Cole", first_name="Cole", last_name="Rutledge", email="cole@email.com", hashed_password="password1")

  db.session.add(user)
  db.session.commit()
