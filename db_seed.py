import csv
from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models import db, User, Posting

csv_file_path = 'indeed_seed.csv'

with open(csv_file_path, newline='', encoding='utf-8-sig') as f:
  next(f)
  reader = csv.reader(f)

  with app.app_context():
    db.drop_all()
    db.create_all()

    for row in reader:
      posting = Posting(
          search_terms=row[0],
          search_loc=row[1],
          title=row[2],
          location=row[3],
          company=row[4],
          salary=row[5],
          date=row[6],
          snippet=row[7][:500],
          description=row[7],
          link=row[8],
      )
      db.session.add(posting)

    db.session.commit()
