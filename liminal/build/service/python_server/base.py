import yaml
from abc import ABCMeta, abstractmethod


class WebFrameworkBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    def start_server(self, yml_path='service.yml'):
        with open(yml_path) as stream:
            self._start_server(yaml.safe_load(stream))

    def _start_server(self, config):
        # self._run_on_startup(config['on_startup'])
        self.add_endpoints(config['endpoints'])
        print('Starting python server')
        self._run_app()

    def add_endpoints(self, endpoints):
        for endpoint_config in endpoints:
            print(f'Registering endpoint: {endpoint_config}')
            endpoint = endpoint_config['endpoint']

            print(endpoint_config['module'])

            module = _get_module(endpoint_config['module'])
            function = module.__getattribute__(endpoint_config['function'])
            self._add_url_rule(endpoint, function)

    @abstractmethod
    def _add_url_rule(self, endpoint, function):
        pass

    @abstractmethod
    def _run_app(self):
        pass

    def _run_on_startup(self, startup_configs):
        pass


def _get_module(kls):
    parts = kls.split('.')
    module = ".".join(parts)
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m