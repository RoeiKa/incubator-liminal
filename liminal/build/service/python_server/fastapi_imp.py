import uvicorn
from fastapi import FastAPI


class FastApiServer(WebFrameworkBase):
    def __init__(self,):
        self.app = FastAPI(title=__name__)

    def _add_url_rule(self, endpoint, function):
        self.app.router.add_api_route(path=endpoint,
                                      endpoint=function,
                                      methods=['GET', 'POST'])

    def _run_app(self):
        uvicorn.run(self.app, host="0.0.0.0", port=80)

    def _run_on_startup(self, startup_configs):
        self.app.router.on_startup.append()


server = FastApiServer().start_server()
