import json, re, html, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FEEDS=[
 ('Maroc','Maroc','https://news.google.com/rss/search?q='+urllib.parse.quote('Maroc actualités when:1d')+'&hl=fr&gl=MA&ceid=MA:fr'),
 ('Économie','Économie','https://news.google.com/rss/search?q='+urllib.parse.quote('économie Maroc entreprises when:1d')+'&hl=fr&gl=MA&ceid=MA:fr'),
 ('Monde','Monde','https://news.google.com/rss/headlines/section/topic/WORLD?hl=fr&gl=FR&ceid=FR:fr'),
 ('Technologies','Technologies','https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=fr&gl=FR&ceid=FR:fr'),
 ('Société','Société','https://news.google.com/rss/search?q='+urllib.parse.quote('société Maroc when:1d')+'&hl=fr&gl=MA&ceid=MA:fr'),
 ('Environnement','Environnement','https://news.google.com/rss/search?q='+urllib.parse.quote('climat environnement when:1d')+'&hl=fr&gl=FR&ceid=FR:fr'),
 ('Culture','Culture','https://news.google.com/rss/headlines/section/topic/ENTERTAINMENT?hl=fr&gl=FR&ceid=FR:fr'),
 ('Sport','Sport','https://news.google.com/rss/headlines/section/topic/SPORTS?hl=fr&gl=FR&ceid=FR:fr')]

def plain(s):
 s=re.sub(r'<[^>]*>',' ',s or '')
 return re.sub(r'\s+',' ',html.unescape(s)).strip()[:420]

def child(e,name):
 v=e.find(name)
 return ''.join(v.itertext()).strip() if v is not None else ''

items=[];seen=set();errors=[]
for category,label,url in FEEDS:
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 TagineVolant/1.0'})
  with urllib.request.urlopen(req,timeout=18) as r: xml=r.read()
  root=ET.fromstring(xml)
  count=0
  for e in root.findall('.//channel/item'):
   title=plain(child(e,'title')); link=child(e,'link'); date=child(e,'pubDate')
   if not title or not link:continue
   key=re.sub(r'\W+','',title.lower())[:100]
   if key in seen:continue
   seen.add(key)
   source=child(e,'source') or (title.rsplit(' - ',1)[-1] if ' - ' in title else 'Google Actualités')
   if source and title.endswith(' - '+source):title=title[:-(len(source)+3)]
   desc=plain(child(e,'description'))
   from email.utils import parsedate_to_datetime
   try:published=parsedate_to_datetime(date).astimezone(timezone.utc).isoformat()
   except:published=datetime.now(timezone.utc).isoformat()
   items.append({'category':category,'title':title,'description':desc if desc!=title else '', 'source':source,'url':link,'published':published})
   count+=1
   if count>=12:break
 except Exception as exc:errors.append(f'{label}: {exc}')

if not items:
 raise SystemExit('Aucune actualité récupérée : '+ '; '.join(errors))
items.sort(key=lambda x:x['published'],reverse=True)
# Preserve representation of categories in front page
selected=[]
for category,_,_ in FEEDS:
 selected.extend([x for x in items if x['category']==category][:5])
selected=sorted(selected,key=lambda x:x['published'],reverse=True)
now=datetime.now(timezone.utc)
out={'updated':now.isoformat(),'items':selected,'feed_errors':errors}
data=ROOT/'data';(data/'archive').mkdir(parents=True,exist_ok=True)
(data/'latest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
day=now.strftime('%Y-%m-%d')
(data/'archive'/f'{day}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
index=data/'archive-index.json'
days=json.loads(index.read_text(encoding='utf-8')) if index.exists() else []
days=sorted(set(days+[day]),reverse=True)
index.write_text(json.dumps(days,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(selected)} actualités, {len(errors)} flux en erreur')
