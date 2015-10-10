from indico.core import signals
from indico.core.plugins import IndicoPluginBlueprint, IndicoPlugin
from indico.web.http_api import HTTPAPIHook
from indicobysession.http_api.hooks.bysession import RegistrantsHook, RegistrantsBySessionHook, RegistrantHook, \
    RegistrantBySessionHook, CheckInHook, SessionCheckInHook

blueprint = IndicoPluginBlueprint('indicobysession', __name__)


class IndicoBySessionPlugin(IndicoPlugin):
    """Indico By Session Plugin

    """
    configurable = False

    def init(self):
        super(IndicoBySessionPlugin, self).init()

        # Register special hooks for the APIs
        self.registerHook(RegistrantHook)
        self.registerHook(RegistrantBySessionHook)

        self.registerHook(RegistrantsHook)
        self.registerHook(RegistrantsBySessionHook)

        self.registerHook(CheckInHook)
        self.registerHook(SessionCheckInHook)


    def registerHook(self,cls):
        l = []
        for hook in HTTPAPIHook.HOOK_LIST:
            if not hook.RE == cls.RE:
                l.append(hook)
            else:
                print "Found duplicate"
        l.append(cls)
        HTTPAPIHook.HOOK_LIST = l

    def get_blueprints(self):
        return blueprint

    @signals.app_created.connect
    def _config(app, **kwargs):
        pass


