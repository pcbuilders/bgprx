from google.appengine.api import urlfetch, urlfetch_errors
import json

def check_is_live(sid):
  try:
    req     = request('/'.join(['http://web.live.bigo.sg', sid]), urlfetch.HEAD)
    if 'location' in req.headers and req.status_code == 302:
      location  = req.headers['location']
    else:
      location  = ''
    return {'status': 'ok', 'status_code': req.status_code, 'location': location}
  except urlfetch_errors.Error as e:
    return error(e)

def get_user_info(sid):
  return get_jsonp('http://web.live.bigo.sg/get?%s&callback=&_=' % sid)

def get_room_info(sid):
  return get_jsonp('http://live.bigo.tv/castinfo?sid=%s&callback=&_=' % sid)

def get_jsonp(url):
  try:
    req     = request(url, urlfetch.GET)
    if req.status_code == 200 and req.content:
      return {'status': 'ok', 'msg': json.loads(req.content[1:-1])}
    else:
      return error(req.content)
  except urlfetch_errors.Error as e:
    return error(e)

def request(url, method):
  return urlfetch.Fetch(url, headers=headers(), follow_redirects=False, deadline=15, method=method)

def headers():
  return {'User-Agent': 'okhttp3'}

def error(e):
  return {'status': 'error', 'msg': str(e)}
