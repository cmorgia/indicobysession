from base import BaseRegistrantsHook, BaseRegistrantHook, BaseCheckInHook


class RegistrantHook(BaseRegistrantHook):
    RE = r'(?P<event>[\w\s]+)/registrant/(?P<registrant_id>[\w\s]+)'


class RegistrantBySessionHook(BaseRegistrantHook):
    RE = r'(?P<event>[\w\s]+)/session/(?P<session>[\w\s]+)/registrant/(?P<registrant_id>[\w\s]+)'

    def _getParams(self):
        super(RegistrantBySessionHook, self)._getParams()
        self._sessionId = self._pathParams['session']

    def export_registrant(self, aw,bysession=None):
        return super(RegistrantBySessionHook, self).export_registrant(aw,self._sessionId)


class RegistrantsHook(BaseRegistrantsHook):
    RE = r'(?P<event>[\w\s]+)/registrants'


class RegistrantsBySessionHook(BaseRegistrantsHook):
    RE = r'(?P<event>[\w\s]+)/session/(?P<session>[\w\s]+)/registrants'

    def _getParams(self):
        super(RegistrantsBySessionHook, self)._getParams()
        self._sessionId = self._pathParams['session']

    def export_registrants(self, aw,bysession=None):
        return super(RegistrantsBySessionHook, self).export_registrants(aw,self._sessionId)


class CheckInHook(BaseCheckInHook):
    RE = r'(?P<event>[\w\s]+)/registrant/(?P<registrant_id>[\w\s]+)/checkin'


class SessionCheckInHook(BaseCheckInHook):
    RE = r'(?P<event>[\w\s]+)/session/(?P<session_id>[\w\s]+)/registrant/(?P<registrant_id>[\w\s]+)/checkin'

    def _getParams(self):
        super(SessionCheckInHook, self)._getParams()
        session_id = self._pathParams["session_id"]
        self._object = self._object.getSession(session_id)


