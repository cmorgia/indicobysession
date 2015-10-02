from MaKaC.conference import ConferenceHolder
from indico.web.http_api.hooks.event import EventBaseHook
from indico.web.http_api.hooks.registration import RegistrantFetcher
from indico.web.http_api.util import get_query_parameter


class BaseRegistrantHook(EventBaseHook):
    METHOD_NAME = 'export_registrant'
    NO_CACHE = True
    DEFAULT_DETAIL = 'basic'

    def _getParams(self):
        super(BaseRegistrantHook, self)._getParams()
        self.auth_key = get_query_parameter(self._queryParams, ["auth_key"])
        self._conf = ConferenceHolder().getById(self._pathParams['event'])
        registrant_id = self._pathParams["registrant_id"]
        self._registrant = self._conf.getRegistrantById(registrant_id)

    def _hasAccess(self, aw):
        return self._conf.canManageRegistration(aw.getUser()) or self._conf.canModify(aw)

    def export_registrant(self, aw, bysession=None):


        expInt = RegistrantFetcher(aw, self)
        result =  expInt.registrant()
        if bysession and not self._registrant.getSession(bysession):
            result["canEnter"] = False
            result["canEnterMessage"] = "The registrant is not approved for this session"
        return result


class BaseRegistrantsHook(EventBaseHook):
    METHOD_NAME = 'export_registrants'
    NO_CACHE = True

    def _getParams(self):
        super(BaseRegistrantsHook, self)._getParams()
        self._conf_id = self._pathParams['event']
        self._conf = ConferenceHolder().getById(self._conf_id)
        self._registrants = self._conf.getRegistrantsList()

    def _hasAccess(self, aw):
        return self._conf.canManageRegistration(aw.getUser()) or self._conf.canModify(aw)

    def export_registrants(self, aw,bysession=None):

        registrant_list = []
        for registrant in self._registrants:
            skip = False

            if bysession:
                sess = registrant.getSession(bysession)
                if sess is None:
                    skip = True
                else:
                    checkedIn = sess.isCheckedIn()
            else:
                checkedIn = registrant.isCheckedIn(),

            if not skip:
                reg = {
                    "registrant_id": registrant.getId(),
                    "checked_in": checkedIn,
                    "full_name": registrant.getFullName(title=True, firstNameFirst=True),
                    "checkin_secret": registrant.getCheckInUUID(),
                }
                if bysession:
                    reg["session"]=bysession
                regForm = self._conf.getRegistrationForm()
                reg["personal_data"] = regForm.getPersonalData().getRegistrantValues(registrant)
                registrant_list.append(reg)
        return {"registrants": registrant_list}


class BaseCheckInHook(EventBaseHook):
    PREFIX = "api"
    METHOD_NAME = 'api_checkin'
    NO_CACHE = True
    COMMIT = True
    HTTP_POST = True

    def _getParams(self):
        super(BaseCheckInHook, self)._getParams()
        self._check_in = get_query_parameter(self._queryParams, ["checked_in"]) == "yes"
        self._secret = get_query_parameter(self._queryParams, ["secret"])
        registrant_id = self._pathParams["registrant_id"]
        self._conf = ConferenceHolder().getById(self._pathParams['event'])
        self._object = self._conf.getRegistrantById(registrant_id)

    def _hasAccess(self, aw):
        return (self._conf.canManageRegistration(aw.getUser()) or self._conf.canModify(aw)) \
            and self._secret == self._object.getCheckInUUID()

    def api_checkin(self, aw):
        if self._object:
            self._object.setCheckedIn(self._check_in)
            checkin_date = format_datetime(self._object.getAdjustedCheckInDate(), format="short") if self._check_in else None

            return {
                "checked_in": self._check_in,
                "checkin_date": checkin_date if self._check_in else None
            }
        else:
            return {"status": "no session has been found"}