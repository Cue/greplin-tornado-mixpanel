# Copyright 2011 The greplin-tornado-mixpanel Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A mixpanel API"""

import urllib
import base64
import time

from tornado import httpclient, escape



class Mixpanel(object):
  """A mixpanel client"""


  BASE_URL = "http://api.mixpanel.com"


  def __init__(self, token, uid, remote_ip):
    self._token = token
    self._uid = uid
    self._remote_ip = remote_ip


  def _call(self, callback, method, params):
    """Make a call to mixpanel"""
    url = "%s/%s?%s" % (self.BASE_URL, method, urllib.urlencode(params))
    http = httpclient.AsyncHTTPClient()
    http.fetch(url, callback)


  def _encode_request(self, event, properties):
    """Encode a request"""
    properties.update({
      'ip':self._remote_ip,
      'token':self._token,
      'time':int(time.time())
    })
    if self._uid:
      properties['distinct_id'] = self._uid
    return base64.b64encode(escape.json_encode({'event':event, 'properties':properties}))


  def track_event(self, event, properties=None, callback=None):
    """Send a tracked event to mixpanel"""
    properties = properties if properties is not None else {}
    callback = callback or (lambda x: True)
    self._call(callback, 'track', {'data':self._encode_request(event, properties)})


  def track_funnel(self, funnel_name, step, goal, properties=None, callback=None):
    """Track a funnel"""
    properties = properties if properties is not None else {}
    callback = callback or (lambda x: True)
    properties.update({
      'funnel':funnel_name,
      'step':step,
      'goal':goal
    })
    self._call(callback, 'track', {'data':self._encode_request('mp_funnel', properties)})

















