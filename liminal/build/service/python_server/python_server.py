#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os

import yaml

from liminal.build.image_builder import ServiceImageBuilderMixin
from liminal.build.python import BasePythonImageBuilder


def implementations():
    return {'flask': {'file_name': 'flask_imp.py',
                      'requirements': 'pyyaml Flask==1.1.1'},
            'fastapi': {'file_name': 'fastapi_imp.py',
                        'requirements': 'pyyaml fastapi==0.63.0 uvicorn==0.13.2'}
            }


class PythonServerImageBuilder(BasePythonImageBuilder, ServiceImageBuilderMixin):
    def __init__(self, config, base_path, relative_source_path, tag):
        super().__init__(config, base_path, relative_source_path, tag)
        self.framework = self._get_framework()

    @staticmethod
    def _dockerfile_path():
        return os.path.join(os.path.dirname(__file__), 'Dockerfile')

    def _additional_files_from_paths(self):
        return [
            os.path.join(os.path.dirname(__file__),
                         'base.py'),
            os.path.join(os.path.dirname(__file__),
                         self.framework['file_name']),
        ]

    def _additional_files_from_filename_content_pairs(self):
        f = super()._additional_files_from_filename_content_pairs()
        data = f[0][1].\
            replace('{{requirements}}', self.framework['requirements']).\
            replace('{{web_framework}}', self.framework['file_name'])

        return [(f[0][0], data)] + \
               [('service.yml', yaml.safe_dump(self.config))]

    def _get_framework(self):
        return implementations()[self.config.get('framework', 'flask')]

