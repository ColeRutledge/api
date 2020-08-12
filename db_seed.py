from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from app import app, db
from app.models import db, User, Posting


with app.app_context():
  db.drop_all()
  db.create_all()

  date = datetime.now()

  user = User(user_name="Cole", first_name="Cole", last_name="Rutledge", email="cole@email.com", hashed_password="password1")
  posting = Posting(job_title="Junior React Engineer", company="Discovery Education", city="Charlotte", state="NC", formatted_location="Charlotte, NC", source="LinkedIn", date=date, snippet="looking for junior react engineer with python experience", url="http://www.indeed.com/viewjob?jk=12345", latitude=30.27127, longitude=-97.74103, job_key="12345", expired=False, indeed_apply=True, ff_location="Charlotte, NC", rel_time="5 hours ago")

  db.session.add(user)
  db.session.add(posting)
  db.session.commit()
