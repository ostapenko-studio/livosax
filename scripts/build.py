"""Build a dependency-free static site from the reviewed public video catalog."""
import json, re, shutil
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
videos=json.loads((ROOT/'videos.json').read_text())
assert videos and len({v['id'] for v in videos})==len(videos)
for v in videos:
 assert re.fullmatch(r'[A-Za-z0-9_-]{11}',v['id'])
 v['name']=v['title'].split(' | ')[0]

def thumbnail(v, featured=False):
 vid=v['id']; name=escape(v['name'],quote=True)
 return f'''<a class="thumbnail {'featured-image' if featured else ''}" href="https://www.youtube.com/watch?v={vid}" data-video="{vid}" data-title="{name}" aria-label="Play {name}"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{name} — Olivia playing alto saxophone" width="480" height="360" {'fetchpriority="high"' if featured else 'loading="lazy"'}><span class="play" aria-hidden="true">▶</span><span class="duration">{escape(v.get('duration',''))}</span></a>'''

cards='\n'.join(f'''<article class="video-card">{thumbnail(v)}<div class="card-meta"><span>ALTO SAXOPHONE</span><a href="https://www.youtube.com/watch?v={v['id']}" target="_blank" rel="noopener">YouTube ↗<span class="sr-only">: {escape(v['name'])}</span></a></div><h3><a href="https://www.youtube.com/watch?v={v['id']}" data-video="{v['id']}" data-title="{escape(v['name'],quote=True)}">{escape(v['name'])}</a></h3></article>''' for v in videos)
first=videos[0]
page='''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>livOsax — Olivia’s saxophone journey</title><meta name="description" content="Follow Olivia’s alto saxophone journey. Watch her performances, discover familiar melodies, and listen along with Essential Elements Book 1."><meta name="theme-color" content="#102638"><link rel="canonical" href="https://livosax.com/"><meta property="og:type" content="website"><meta property="og:title" content="livOsax — Olivia’s saxophone journey"><meta property="og:description" content="Learning, practising, and sharing. One song at a time."><meta property="og:url" content="https://livosax.com/"><link rel="icon" href="assets/livOsax-icon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="app.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-header wrap"><a class="brand" href="./" aria-label="livOsax home"><img src="assets/livOsax-icon.png" alt="" width="56" height="56"><span>liv<span class="gold">O</span>sax</span></a><nav aria-label="Main navigation"><a href="#videos">Performances</a><a href="#about">About Olivia</a><a class="button small" href="https://www.youtube.com/@livosax?sub_confirmation=1" target="_blank" rel="noopener">YouTube <span aria-hidden="true">↗</span></a></nav></header>
<main id="main"><section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">OLIVIA’S SAXOPHONE JOURNEY</p><h1 id="hero-title">One song<br>at a <em>time.</em></h1><p class="intro">Learning, practising, and sharing the sound of the alto saxophone.</p><a class="text-link" href="#videos">Explore the performances <span aria-hidden="true">↓</span></a></div><div class="featured"><div class="featured-label"><span class="eyebrow">THE LATEST PERFORMANCE</span><span class="tiny">01 / '''+str(len(videos)).zfill(2)+'''</span></div>'''+thumbnail(first,True)+'''<div class="featured-caption"><h2>'''+escape(first['name'])+'''</h2><span>Essential Elements · Book 1</span></div></div></section>
<section id="videos" class="library wrap" aria-labelledby="library-title"><div class="section-heading"><div><p class="eyebrow">THE VIDEO COLLECTION</p><h2 id="library-title">Little pieces. Big progress.</h2><p>Familiar melodies and new challenges from Essential Elements Book 1.</p></div><span class="count">'''+str(len(videos))+''' performances</span></div><div class="video-grid">'''+cards+'''</div><a class="text-link all-youtube" href="https://www.youtube.com/@livosax/videos" target="_blank" rel="noopener">Visit the full channel on YouTube ↗</a></section>
<section id="about" class="about" aria-labelledby="about-title"><div class="wrap about-inner"><div><p class="eyebrow">MEET THE MUSICIAN</p><h2 id="about-title">Hello, I’m Olivia.</h2></div><div><p>I’m learning the alto saxophone, one piece at a time. This is where I share my performances and the music I’m practising along the way.</p><p>Whether you’re learning too, helping someone practise, or just here to listen—welcome.</p><a class="button" href="https://www.youtube.com/@livosax?sub_confirmation=1" target="_blank" rel="noopener">Follow my journey on YouTube ↗</a></div></div></section></main>
<footer class="wrap"><a class="brand" href="./"><img src="assets/livOsax-icon.png" alt="" width="40" height="40"><span>liv<span class="gold">O</span>sax</span></a><p>Olivia’s saxophone journey.</p><a href="https://www.youtube.com/@livosax" target="_blank" rel="noopener">YouTube ↗</a></footer>
<dialog id="player" aria-labelledby="player-title"><div class="player-header"><h2 id="player-title">Performance</h2><button id="close-player" aria-label="Close video">×</button></div><div id="player-frame"></div><p class="player-note">Playing from YouTube. <a id="youtube-fallback" href="https://www.youtube.com/@livosax" target="_blank" rel="noopener">Watch on YouTube ↗</a></p></dialog></body></html>'''
(ROOT/'index.html').write_text(page)
out=ROOT/'dist';out.mkdir(exist_ok=True)
for f in ['index.html','style.css','app.js','CNAME','robots.txt','sitemap.xml','.nojekyll']:
 shutil.copy2(ROOT/f,out/f)
shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True)
print(f'Built {len(videos)} performances into dist/')
import seo
seo.build(ROOT,videos)
