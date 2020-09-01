from flask import Blueprint, jsonify, render_template
from app.models import db, AvgMktSalary, MarketMetric

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
  return render_template('index.pug')


@bp.route('/avgmktsalaries')
def get_avg_mkt_sals():
  print()
  print('********GETTING AVG SALARIES********')
  print()

  salaries = AvgMktSalary.query.order_by(AvgMktSalary.search_loc).all()

  data = {
      'javascript': {
          'avg_salaries': [round(sal.formatted_sal / 1000, 1) for sal in salaries if sal.search_terms == 'javascript developer'],
          'labels': sorted(list(set([sal.search_loc for sal in salaries]))),
      },
      'python': {
          'avg_salaries': [round(sal.formatted_sal / 1000, 1) for sal in salaries if sal.search_terms == 'python developer'],
          'labels': sorted(list(set([sal.search_loc for sal in salaries]))),
      },
  }

  return jsonify(data), 200


@bp.route('/mktmetrics')
def get_mkt_metrics():
  print()
  print('********GETTING METRICS********')
  print()

  metrics = MarketMetric.query.order_by(MarketMetric.search_loc).all()
  js_data = [metric.pos_counts_mkt for metric in metrics if metric.search_terms == 'javascript developer']
  py_data = [metric.pos_counts_mkt for metric in metrics if metric.search_terms == 'python developer']

  data = {
      'javascript': {
          'mkt_pct': [round(num / sum(js_data) * 100, 1) for num in js_data],
          'labels': sorted(list(set([metric.search_loc for metric in metrics]))),
          'pos_counts': js_data,
      },
      'python': {
          'mkt_pct': [round(num / sum(py_data) * 100, 1) for num in py_data],
          'labels': sorted(list(set([metric.search_loc for metric in metrics]))),
          'pos_counts': py_data,
      },
  }

  return jsonify(data), 200
