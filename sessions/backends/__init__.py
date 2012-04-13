import uuid

from flask.session import SessionMixin
from werkzeug.contrib.sessions import ModificationTrackingDict

FLASK_SESSION_COOKIE_NAME = 'FLASK_SESSION_COOKIE_NAME'

class SessionBase(SessionMixin, ModificationTrackingDict):
    
    def __init__(self, data=None, session_key=None):
        super(SessionBase, self).__init__(data or ())
        if not session_key:
            session_key = str(uuid.uuid4())
        
        self._session_key = session_key
    
    @property
    def session_key(self):
        return self._session_key

    