import csv
from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models import db, User, Posting, AvgMktSalary, MarketMetric

seed_positions_path = 'seed_positions.csv'
seed_pos_metrics_mkt_path = 'seed_pos_metrics_mkt.csv'
seed_market_sals_path = 'seed_market_sals.csv'

with app.app_context():
  db.drop_all()
  db.create_all()

  with open(seed_positions_path, newline='', encoding='utf-8-sig') as f:
    next(f)
    reader = csv.reader(f)

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
          js_count=row[9],
          python_count=row[10],
          formatted_sal=row[11] or None,
          # formatted_sal=int(float(row[11])) if row[11] else 0,
      )
      db.session.add(posting)

  with open(seed_pos_metrics_mkt_path, newline='', encoding='utf-8-sig') as f:
    next(f)
    reader = csv.reader(f)

    for row in reader:
      mkt_metric = MarketMetric(
          search_loc=row[1],
          search_terms=row[2],
          pos_counts_mkt=row[3],
          pos_pcts_mkt=row[4],
          pos_overall_mkt_pct=row[5],
      )
      db.session.add(mkt_metric)

  with open(seed_market_sals_path, newline='', encoding='utf-8-sig') as f:
    next(f)
    reader = csv.reader(f)

    for row in reader:
      avg_salary = AvgMktSalary(
          search_loc=row[0],
          search_terms=row[1],
          formatted_sal=row[2],
      )
      db.session.add(avg_salary)

  db.session.commit()
