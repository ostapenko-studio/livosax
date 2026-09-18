"""Notify IndexNow of published canonical URLs, after checking the public key."""
import json,urllib.request,xml.etree.ElementTree as E
from pathlib import Path
root=Path(__file__).resolve().parents[1]
key=(root/'indexnow-key.txt').read_text().strip()
key_url=f'https://livosax.com/{key}.txt'
assert urllib.request.urlopen(key_url,timeout=30).read().decode().strip()==key,'Public verification key not live yet'
urls=[n.text for n in E.parse(root/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
data=json.dumps({'host':'livosax.com','key':key,'keyLocation':key_url,'urlList':urls}).encode()
req=urllib.request.Request('https://api.indexnow.org/indexnow',data=data,headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=30) as r:print(f'IndexNow accepted {len(urls)} URLs: HTTP {r.status}')
