"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request, jsonify
import helpers
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
  """Return a friendly HTTP greeting."""
  is_live   = request.args.get('is_live')
  room_info = request.args.get('room_info')
  user_info = request.args.get('user_info')
  
  if is_live:
    return jsonify(**helpers.check_is_live(is_live))
  elif room_info:
    return jsonify(**helpers.get_room_info(room_info))
  elif user_info:
    return jsonify(**helpers.get_user_info(user_info))
  return jsonify(**helpers.error("Don't know what to do :(")), 404


@app.errorhandler(404)
def page_not_found(e):
  """Return a custom 404 error."""
  return jsonify(**helpers.error("Sorry, Nothing at this URL.")), 404

@app.errorhandler(500)
def application_error(e):
  """Return a custom 500 error."""
  return jsonify(**helpers.error('Sorry, unexpected error: {}'.format(e))), 500
