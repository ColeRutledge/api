from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from datetime import datetime
import json
from app.models import db, Posting

bp = Blueprint('posting', __name__, url_prefix="/api/posting")


@bp.route('/', strict_slashes=False, methods=['GET', 'POST'])
@jwt_required
def get_posts():
  print()
  print('********FETCH POSTINGS********')
  print()

  senior_filters = [
      '.net',
      'net',
      'dot net',
      'dotnet',
      'qa ',
      'c++',
      'ios',
      'devops',
      'android',
      'c#',
      'senior',
      'lead',
      'sr ',
      'sr. ',
      'manager',
      'architect',
      'director',
      'php',
      'tableau',
  ]

  consulting_filters = [
      '.net',
      'net',
      'dot net',
      'dotnet',
      'qa ',
      'c++',
      'ios',
      'devops',
      'android',
      'c#',
      'php',
      'tableau',
      'consulting',
      'consultant',
      'w2',
      'contract',
      'contracting',
      'co-op',
  ]

  combined = [
      'senior',
      'lead',
      'sr ',
      'sr. ',
      'manager',
      'architect',
      'director',
      '.net',
      'net',
      'dot net',
      'dotnet',
      'qa ',
      'c++',
      'ios',
      'devops',
      'android',
      'c#',
      'php',
      'tableau',
      'consulting',
      'consultant',
      'w2',
      'contract',
      'contracting',
  ]

  default_filters = [
      '.net',
      'net',
      'dot net',
      'dotnet',
      'qa ',
      'c++',
      'ios',
      'devops',
      'android',
      'c#',
      'php',
      'tableau',
  ]

  if request.method == 'POST':
    data = request.get_json()
    if data['no_filter']:
      filters = None
    elif data['senior_filter'] and not data['consulting_filter']:
      filters = [Posting.title.ilike(f'%{condition}%') for condition in senior_filters]
    elif data['consulting_filter'] and not data['senior_filter']:
      filters = [Posting.title.ilike(f'%{condition}%') for condition in consulting_filters]
    elif data['senior_filter'] and data['consulting_filter']:
      filters = [Posting.title.ilike(f'%{condition}%') for condition in combined]
    else:
      filters = [Posting.title.ilike(f'%{condition}%') for condition in default_filters]
  else:
    filters = [Posting.title.ilike(f'%{condition}%') for condition in combined]

  postings = Posting.query.filter(~or_(*filters)) if filters else Posting.query.all()

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
      'js_count': posting.js_count,
      'python_count': posting.python_count,
  } for posting in postings]
  # } for posting in postings if search in posting.search_terms and posting.js_count > 1]

  return jsonify(res), 200
