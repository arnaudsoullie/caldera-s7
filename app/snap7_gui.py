import logging
from aiohttp_jinja2 import template

from app.service.auth_svc import for_all_public_methods, check_authorization
from app.utility.base_world import BaseWorld
from plugins.snap7.app.snap7_svc import Snap7Service


@for_all_public_methods(check_authorization)
class Snap7GUI(BaseWorld):

    def __init__(self, services, name, description):
        self.name = name
        self.description = description
        self.services = services
        self.snap7_svc = Snap7Service(services)

        self.auth_svc = services.get('auth_svc')
        self.log = logging.getLogger('snap7_gui')

    @template('snap7.html')
    async def splash(self, request):
        return dict(name=self.name, description=self.description)

    # Add functions here that the front-end will use

