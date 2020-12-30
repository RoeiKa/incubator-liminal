
from flask import Flask


class FlaskApiServer(WebFrameworkBase):
    def __init__(self):
        self.app = Flask(__name__)

    def _add_url_rule(self, endpoint, function):
        self.app.add_url_rule(rule=endpoint,
                              endpoint=endpoint,
                              view_func=function,
                              methods=['GET', 'POST'])

    def _run_app(self):
        self.app.run(host='0.0.0.0', threaded=False, port=80)

    def _run_on_startup(self, startup_configs):
        self.app.before_first_request()


FlaskApiServer().start_server()
