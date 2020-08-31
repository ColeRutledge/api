from flask import Flask, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from datetime import datetime
import json
from app.models import db, Posting

bp = Blueprint('posting', __name__, url_prefix="/api/posting")


@bp.route('/', strict_slashes=False, methods=['GET'])
@jwt_required
def get_posts():
  print()
  print('********FETCH POSTINGS********')
  print()
  # search = 'python developer'
  # search_count = 'python_count'
  search = 'javascript developer'
  search_count = 'js_count'

  conditions = [
      '.net',
      'dot net',
      'dotnet',
      'java ',
      'java,',
      'qa ',
      'c++',
      'ios',
      'devops',
      'android',
      'c#',
      'senior',
      'lead',
      'manager',
      'architect',
      'director',
      'php',
      'tableau',
  ]

  filters = [Posting.title.ilike(f'%{condition}%') for condition in conditions]
  postings = Posting.query.filter(~or_(*filters))

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
  } for posting in postings if search in posting.search_terms and posting.js_count > 1]

  return jsonify(res), 200
