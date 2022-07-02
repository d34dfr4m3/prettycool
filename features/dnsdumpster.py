#!/usr/bin/python3
class dnsdumpster:
  def __init__(self,token, target_host):
    self.target_host = target_host
    self.token = token
    self.url="https://dnsdumpster.com/" 

  def enum(self):
    import requests

targetip=sys.argv[1]
csrfmiddlewaretoken='shit_token_here'
data=requests.post(url, data={'targetip': targetip,'csrfmiddlewaretoken':csrfmiddlewaretoken})


print(data.text)

"""
<div id="summary">
  <h1>Forbidden <span>(403)</span></h1>
  <p>CSRF verification failed. Request aborted.</p>

  <p>You are seeing this message because this HTTPS site requires a &#39;Referer header&#39; to be sent by your Web browser, but none was sent. This header is required for security reasons, to ensure that your browser is not being hijacked by third parties.</p>
  <p>If you have configured your browser to disable &#39;Referer&#39; headers, please re-enable them, at least for this site, or for HTTPS connections, or for &#39;same-origin&#39; requests.</p>
  <p>If you are using the &lt;meta name=&quot;referrer&quot; content=&quot;no-referrer&quot;&gt; tag or including the &#39;Referrer-Policy: no-referrer&#39; header, please remove them. The CSRF protection requires the &#39;Referer&#39; header to do strict referer checking. If you&#39;re concerned about privacy, use alternatives like &lt;a rel=&quot;noreferrer&quot; ...&gt; for links to third-party sites.</p>


</div>
"""


import sys
