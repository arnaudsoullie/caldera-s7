from app.utility.base_world import BaseWorld
from plugins.snap7.app.snap7_gui import Snap7GUI
from plugins.snap7.app.snap7_api import Snap7API

name = 'Snap7'
description = 'Snap7 plugin for caldera'
address = '/plugin/snap7/gui'
access = BaseWorld.Access.RED


async def enable(services):
    app = services.get('app_svc').application
    snap7_gui = Snap7GUI(services, name=name, description=description)
    app.router.add_static('/snap7', 'plugins/snap7/static/', append_version=True)
    app.router.add_route('GET', '/plugin/snap7/gui', snap7_gui.splash)

    snap7_api = Snap7API(services)
    # Add API routes here
    app.router.add_route('POST', '/plugin/snap7/mirror', snap7_api.mirror)

