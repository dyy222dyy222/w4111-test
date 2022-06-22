#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.



A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import application.restaurant
import application.platform
import application.deliveryman
import application.customer
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://wh2502:25022546@35.196.192.139/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  return render_template("home.html")


@app.route('/restaurant/', methods=["GET"])
def restaurant_render():
  return render_template("restaurant.html")

@app.route('/peak_hours', methods=["POST"])
def search_peak_hours():
  rows = ["restaurant_name", "order_hour", "total_orders_per_hour"]
  print(str(request.form))
  query = application.restaurant.fetch_peak_hours(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  if len(result) == 0:
    return render_template("no_result.html")
  else:
    return render_template("peak_hours_view.html", **dict(res = result))


@app.route('/menu_design', methods=["POST"])
def search_menu_design():
  rows = ["item_name", "order_times"]
  print(str(request.form))
  query = application.restaurant.fetch_menu_design(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("menu_design_view.html", **dict(res = result))


@app.route('/churn_rate', methods=["POST"])
def search_churn_rate():
  rows = ["restaurant_name", "monthly_churn_rate"]
  print(str(request.form))
  query = application.restaurant.fetch_churn_rate(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("churn_rate_view.html", **dict(res = result))

@app.route('/avg_number_of_reservation', methods=["POST"])
def search_avg_reservation():
  rows = ["customer_id", "number_of_reservation", "more_than_avg"]
  print(str(request.form))
  query = application.restaurant.fetch_avg_res(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("number_of_reservation_view.html", **dict(res = result))

@app.route('/platform/', methods=["GET"])
def platform_render():
  return render_template("platform.html")

@app.route('/percentage_coupon_used', methods=["POST"])
def search_pct_coupon():
  rows = ["percentage_coupon_used", "pct"]
  print(str(request.form))
  query = application.platform.fetch_pct_coupon(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("percentage_of_coupon_used_view.html", **dict(res = result))

@app.route('/comparison_ordernumber_consumption_coupon', methods=["POST"])
def search_before_after():
  rows = ["whether_use_coupon", "avg_order_number", "avg_consumption_amount"]
  print(str(request.form))
  query = application.platform.fetch_before_after(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("before_after_view.html", **dict(res = result))

@app.route('/number_of_reservations_in_each_city', methods=["POST"])
def search_customer_distribution():
  rows = ["city", "number_of_orders"]
  print(str(request.form))
  query = application.platform.fetch_customer_distribution(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("number_of_reservations_in_each_city_view.html", **dict(res = result))

@app.route('/deliveryman/', methods=["GET"])
def delivery_render():
  return render_template("deliveryman.html")

@app.route('/avg_delivery_time_tip', methods=["POST"])
def search_deliveryman():
  rows = ["deliveryman_name", "avg_delivery_time", "avg_delivery_tips"]
  print(str(request.form))
  query = application.deliveryman.fetch_deliveryman(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("deliveryman_view.html", **dict(res = result))


@app.route('/customer/', methods=["GET"])
def customer_render():
  return render_template("customer.html")

@app.route('/popular_restaurant', methods=["POST"])
def search_popular_restaurant():
  rows = ["restaurant_name", "number_of_reservations", "avg_base_amount"]
  print(str(request.form))
  query = application.customer.fetch_popular_restaurant(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("popular_restaurant_view.html", **dict(res = result))

@app.route('/popular_dish', methods=["POST"])
def search_popular_dish():
  rows = ["item_name", "number_of_orders"]
  print(str(request.form))
  query = application.customer.fetch_popular_dish(request.form)
  print(query)
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(dict(zip(rows, c)))
  return render_template("popular_dish_view.html", **dict(res = result))


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
