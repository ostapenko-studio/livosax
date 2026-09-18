"""Generate crawlable watch pages and truthful video/search metadata."""
import json,re,secrets,shutil
from html import escape as h
from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,ElementTree,register_namespace
from datetime import datetime
BASE='https://livosax.com'

def build(root,videos):
 out=root/'dist'
 page=(root/'index.html').read_text()
 for v in videos:
  old=f'''<h3><a href="https://www.youtube.com/watch?v={v['id']}" data-video="{v['id']}" data-title="{h(v['name'],quote=True)}">'''
  page=page.replace(old,f'''<h3><a href="/videos/{v['slug']}/">''')
 website={'@context':'https://schema.org','@graph':[{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'livOsax','description':'Olivia’s alto saxophone performances.','inLanguage':'en-AU'}, {'@type':'ItemList','name':'Olivia’s alto saxophone performances','itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+'/videos/'+v['slug']+'/','name':v['name']} for i,v in enumerate(videos)]}]}
 page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(website,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')
 (root/'index.html').write_text(page);(out/'index.html').write_text(page)
 header=re.search(r'<header class="site-header.*?</header>',page,re.S).group().replace('href="./"','href="/"').replace('href="#','href="/#')
 footer=re.search(r'<footer.*?</footer>',page,re.S).group().replace('href="./"','href="/"')
 header=header.replace('src="assets/','src="/assets/');footer=footer.replace('src="assets/','src="/assets/')
 sm='http://www.sitemaps.org/schemas/sitemap/0.9';vn='http://www.google.com/schemas/sitemap-video/1.1'
 register_namespace('',sm);register_namespace('video',vn)
 sitemap=Element('{'+sm+'}urlset');SubElement(SubElement(sitemap,'{'+sm+'}url'),'{'+sm+'}loc').text=BASE+'/'
 for v in videos:
  url=BASE+'/videos/'+v['slug']+'/'
  title=v['name']+' | Alto Saxophone Performance | livOsax'
  thumb='https://i.ytimg.com/vi/'+v['id']+'/hqdefault.jpg'
  embed='https://www.youtube-nocookie.com/embed/'+v['id']
  pub=datetime.fromisoformat(v['published']).strftime('%d %B %Y')
  exercise=re.search(r'#(\d+)',v['name']).group(1)
  schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':url,'url':url,'name':title,'description':v['summary'],'inLanguage':'en-AU','mainEntity':{'@id':url+'#video'}},{'@type':'VideoObject','@id':url+'#video','name':v['title'],'description':v['summary'],'thumbnailUrl':[thumb],'uploadDate':v['published'],'duration':f"PT{v['seconds']}S",'embedUrl':embed,'url':url,'inLanguage':'en','isFamilyFriendly':True,'publisher':{'@type':'Organization','name':'livOsax','url':BASE+'/','sameAs':['https://www.youtube.com/@livosax']}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'livOsax','item':BASE+'/'},{'@type':'ListItem','position':2,'name':v['name'],'item':url}]}]}
  related=''.join(f'<a href="/videos/{other["slug"]}/">{h(other["name"])}</a>' for other in videos if other['id']!=v['id'])
  html=f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{h(title)}</title><meta name="description" content="{h(v['summary'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1"><link rel="canonical" href="{url}"><meta property="og:type" content="video.other"><meta property="og:title" content="{h(title,quote=True)}"><meta property="og:description" content="{h(v['summary'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{thumb}"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/livOsax-icon.svg"><link rel="stylesheet" href="/style.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script></head><body><a class="skip" href="#main">Skip to content</a>{header}<main id="main" class="wrap watch-page"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">livOsax</a><span aria-hidden="true">/</span><span>{h(v['name'])}</span></nav><p class="eyebrow">ALTO SAXOPHONE · ESSENTIAL ELEMENTS BOOK 1</p><h1>{h(v['name'])}</h1><p class="watch-summary">{h(v['summary'])}</p><div class="watch-player"><iframe src="{embed}?rel=0" title="{h(v['title'],quote=True)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div><div class="watch-meta"><span>Published <time datetime="{v['published']}">{pub}</time> · {v['duration']}</span><a href="https://www.youtube.com/watch?v={v['id']}" target="_blank" rel="noopener">Watch on YouTube ↗</a></div><section class="piece-notes"><h2>About this performance</h2><p>{h(v['summary'])} This recording is a listening reference for parents, teachers and beginning saxophone players practising the same exercise.</p><dl><div><dt>Performer</dt><dd>Olivia · livOsax</dd></div><div><dt>Instrument</dt><dd>E-flat alto saxophone</dd></div><div><dt>Book</dt><dd>Essential Elements for Band, Book 1</dd></div><div><dt>Exercise</dt><dd>#{exercise}</dd></div></dl><h2>Listening along</h2><h3>What piece is Olivia playing?</h3><p>{h(v['name'])}, exercise {exercise} in Essential Elements for Band – E-flat Alto Saxophone, Book 1.</p><h3>Can I use this video while practising?</h3><p>You can listen to this performance alongside your own copy of the exercise. It is a student performance, rather than a lesson or a substitute for your teacher’s guidance.</p><h3>Where can I hear more?</h3><p>Browse <a href="/#videos">Olivia’s performances</a> or visit <a href="https://www.youtube.com/@livosax">livOsax on YouTube</a>.</p></section><section class="related"><h2>More from Olivia</h2><div>{related}</div></section></main>{footer}</body></html>'''
  folder=out/'videos'/v['slug'];folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(html)
  node=SubElement(sitemap,'{'+sm+'}url');SubElement(node,'{'+sm+'}loc').text=url
  video=SubElement(node,'{'+vn+'}video')
  for tag,value in [('thumbnail_loc',thumb),('title',v['title']),('description',v['summary']),('player_loc',embed),('duration',str(v['seconds'])),('publication_date',v['published']),('family_friendly','yes')]:SubElement(video,'{'+vn+'}'+tag).text=value
 ElementTree(sitemap).write(out/'sitemap.xml',encoding='utf-8',xml_declaration=True);shutil.copy2(out/'sitemap.xml',root/'sitemap.xml')
 keyfile=root/'indexnow-key.txt'
 if not keyfile.exists():keyfile.write_text(secrets.token_hex(16))
 key=keyfile.read_text().strip();(out/(key+'.txt')).write_text(key)
 notfound='<!doctype html><html lang="en-AU"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found | livOsax</title><link rel="stylesheet" href="/style.css"><main class="wrap watch-page"><h1>That page isn’t here.</h1><p><a class="text-link" href="/">Return to Olivia’s performances</a></p></main></html>'
 (out/'404.html').write_text(notfound)
 for f in root.glob('google*.html'):shutil.copy2(f,out/f.name)
 if (root/'BingSiteAuth.xml').exists():shutil.copy2(root/'BingSiteAuth.xml',out/'BingSiteAuth.xml')
 print(f'Generated {len(videos)} watch pages, video sitemap, schema and IndexNow verification file.')
