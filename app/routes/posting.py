from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from data import json_data
import json
from app.models import db, Posting

bp = Blueprint('posting', __name__, url_prefix="/api/posting")


@bp.route('/', strict_slashes=False, methods=['GET'])
def get_posts():
  print()
  print('********GETTING POSTINGS********')
  print()

  postings = Posting.query.order_by(Posting.state).all()
  res = [{
      'id': posting.id,
      'job_title': posting.job_title,
      'company': posting.company,
      'city': posting.city,
      'state': posting.state,
      'url': posting.url,
  } for posting in postings]
  return jsonify(res), 200


@bp.route('/add', methods=['GET'])
def create_posts():
  print()
  print('********CREATING POSTINGS********')
  print()

  res = json.loads(json_data)
  postings = res['results']
  for i in range(len(postings)):
    posting = postings[i]
    date = datetime.strptime(posting['date'], '%a, %d %b %Y %H:%M:%S %Z')
    new_posting = Posting(
        id=len(Posting.query.all()) + 1,
        job_title=posting['jobtitle'],
        company=posting['company'],
        city=posting['city'],
        state=posting['state'],
        formatted_location=posting['formattedLocation'],
        source=posting['source'],
        date=date,
        snippet=posting['snippet'],
        url=posting['url'],
        latitude=posting['latitude'],
        longitude=posting['longitude'],
        job_key=posting['jobkey'],
        expired=posting['expired'],
        indeed_apply=posting['indeedApply'],
        ff_location=posting['formattedLocationFull'],
        rel_time=posting['formattedRelativeTime'],
    )
    db.session.add(new_posting)

  db.session.commit()
  return {'message': 'success!'}, 201
