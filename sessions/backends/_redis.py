
import cPickle as pickle

from flask.session import SessionInterface
from sessions.backends import SessionBase, FLASK_SESSION_COOKIE_NAME

try:
    import redis.client
except ImportError, ie:
    print "Unable to import a redis client.  Make sure you have a proper redis client installed."

def get_redis_client():
    client = redis.client.Redis()
    return client

def set_session_data(session_key, data):
    client = get_redis_client()
    
    if not session_key:
        return
    
    if not data:
        data = {}
    
    client.set('session:%s' % session_key, pickle.dumps(data))

def get_session_data(session_key):
    client = get_redis_client()
    
    if not session_key:
        return {}
    
    data = client.get('session:%s' % session_key)
    if not data:
        return {}

    return pickle.loads(data)

class RedisSession(SessionBase):
    
    @classmethod
    def load(cls, session_key):
        data = get_session_data(session_key)
        rs = RedisSession(session_key=session_key, data=data)
        return rs
    
    def save(self):
        set_session_data(self.session_key, dict(self))

class RedisSessionBackend(SessionInterface):
    session_class = RedisSession

    def open_session(self, app, request):
        return self.session_class.load(request.cookies.get(FLASK_SESSION_COOKIE_NAME, None))

    def save_session(self, app, session, response):
        response.set_cookie(FLASK_SESSION_COOKIE_NAME, session.session_key)
        session.save()
