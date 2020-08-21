from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func, not_, or_
from datetime import datetime
import json
from app.models import db, Posting

bp = Blueprint('posting', __name__, url_prefix="/api/posting")


@bp.route('/', strict_slashes=False, methods=['GET'])
def get_posts():
  print()
  print('********FETCH POSTINGS********')
  print()
  # conditions = ['.net', '.NET', '.Net', '.Net Developer']

  # postings = Posting.query.all()
  postings = Posting.query.filter(~or_(
      Posting.title.ilike('%.net%'),
      Posting.title.ilike('%java %'),
      Posting.title.ilike('%devops %'),
      Posting.title.ilike('%qa %'),
      Posting.title.ilike('%senior%'),
      Posting.title.ilike('%lead%'),
      Posting.title.ilike('%architect%'),
      Posting.title.ilike('%manager%'),
      Posting.title.ilike('%director%'),
      Posting.title.ilike('%c++%'),
      Posting.title.ilike('%ios%'),
      Posting.title.ilike('%android%'),
      Posting.title.ilike('%c#%'),
  ))

  res = [{
      'id': posting.id,
      'search_terms': posting.search_terms,
      'search_loc': posting.search_loc,
      'title': posting.title,
      'location': posting.location,
      'company': posting.company,
      'salary': posting.salary,
      'date': posting.date,
      'snippet': posting.snippet,
      'description': posting.description,
      'link': posting.link,
  } for posting in postings]
  return jsonify(res), 200
