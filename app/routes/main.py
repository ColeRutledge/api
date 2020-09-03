from flask import Blueprint, jsonify, render_template
from app.models import db, AvgMktSalary, MarketMetric

bp = Blueprint('index', __name__)
colors = [
    'rgba(247, 223, 30, 0.4)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 99, 132, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(30, 76, 118, 0.2)',
    'rgba(211, 78, 24, 0.2)',
    'rgba(169, 205, 54, 0.2)',
    'rgba(255, 139, 148, 0.2)',
    'rgba(255, 240, 219, 0.2)',
]


@bp.route('/')
def index():
  return render_template('index.pug')


@bp.route('/avgmktsalaries')
def get_avg_mkt_sals():
  print()
  print('********GETTING AVG SALARIES********')
  print()

  salaries = AvgMktSalary.query.order_by(AvgMktSalary.search_loc).all()
  labels = sorted(list(set([sal.search_loc for sal in salaries])))

  data = {
      'javascript': {
          'avg_salaries': [round(sal.formatted_sal / 1000, 1) for sal in salaries
                           if sal.search_terms == 'javascript developer'],
          'labels': labels,
      },
      'python': {
          'avg_salaries': [round(sal.formatted_sal / 1000, 1) for sal in salaries
                           if sal.search_terms == 'python developer'],
          'labels': labels,
      },
      'ruby': {
          'avg_salaries': [round(sal.formatted_sal / 1000, 1) for sal in salaries
                           if sal.search_terms == 'ruby developer'],
          'labels': labels,
      },
      'java': {
          'avg_salaries': [round(sal.formatted_sal / 1000, 1) for sal in salaries
                           if sal.search_terms == 'java developer'],
          'labels': labels,
      },
  }

  return jsonify(data), 200


@bp.route('/mktmetrics')
def get_mkt_metrics():
  print()
  print('********GETTING METRICS********')
  print()

  metrics = MarketMetric.query.order_by(MarketMetric.search_loc).all()
  js_data = [metric.pos_counts_mkt for metric in metrics
             if metric.search_terms == 'javascript developer']
  py_data = [metric.pos_counts_mkt for metric in metrics
             if metric.search_terms == 'python developer']
  labels = sorted(list(set([metric.search_loc for metric in metrics])))
  background_colors = [color for _, color in zip(labels, colors)]

  data = {
      'javascript': {
          'mkt_pct': [round(num / sum(js_data) * 100, 1) for num in js_data],
          'labels': labels,
          'pos_counts': js_data,
          'background_color': background_colors,
      },
      'python': {
          'mkt_pct': [round(num / sum(py_data) * 100, 1) for num in py_data],
          'labels': labels,
          'pos_counts': py_data,
          'background_color': background_colors,
      },
  }

  return jsonify(data), 200
