#!/usr/bin/env python3
"""GitHub-hosted live activity SVG, no third-party badge or graph servers.

Uses public GitHub REST endpoints, with the built-in GITHUB_TOKEN when available.
The timeline counts public GitHub *events*, not all GitHub contributions or
individual commits. GitHub exposes only recent events (up to ~300), so sparse
history may be incomplete; the SVG explicitly labels that limitation.

Run: GITHUB_TOKEN=... python scripts/update_activity.py
Offline preview: python scripts/update_activity.py --placeholder
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

USERNAME='HsHs-dev'
OUT=Path(__file__).resolve().parents[1]/'assets'
OUT.mkdir(exist_ok=True)

def api(endpoint):
    token=os.environ.get('GITHUB_TOKEN','')
    headers={
       'User-Agent':'HsHs-dev-systems-lab-activity-svg',
       'Accept':'application/vnd.github+json',
       'X-GitHub-Api-Version':'2022-11-28',
    }
    if token: headers['Authorization']=f'Bearer {token}'
    req=Request('https://api.github.com'+endpoint,headers=headers)
    with urlopen(req,timeout=20) as response:
        return json.load(response)

def collect():
    profile=api(f'/users/{USERNAME}')
    repos=[]
    for page in range(1,7):
        chunk=api(f'/users/{USERNAME}/repos?type=owner&sort=pushed&direction=desc&per_page=100&page={page}')
        repos.extend(r for r in chunk if not r.get('fork'))
        if len(chunk)<100: break
    events=[]
    for page in range(1,4):
        chunk=api(f'/users/{USERNAME}/events/public?per_page=100&page={page}')
        events.extend(chunk)
        if len(chunk)<100: break
    now=datetime.now(timezone.utc)
    yesterday=now-timedelta(days=30)
    datecounts=Counter()
    for event in events:
        try: stamp=datetime.fromisoformat(event['created_at'].replace('Z','+00:00'))
        except (KeyError,ValueError): continue
        if stamp>=now-timedelta(days=27): datecounts[stamp.date().isoformat()]+=1
    recent=[r for r in repos if (r.get('pushed_at') or '') >= yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')]
    featured=[r['name'] for r in repos[:3] if r.get('name')]
    return dict(
        repos=profile.get('public_repos',len(repos)),
        stars=sum(r.get('stargazers_count') or 0 for r in repos),
        followers=profile.get('followers',0),
        pushed=len(recent),
        events=datecounts,
        latest=featured,
        refreshed=now.strftime('%d %b %Y · %H:%M UTC'),
        range_label='LAST 28 DAYS',
        pending=False,
    )

def rect(x,y,w,h,r,fill,stroke='none',extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'

def tx(x,y,t,fill,size=16,weight=400,anchor='start',family='Segoe UI,Arial,sans-serif',extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="{family}" {extra}>{escape(str(t))}</text>'

def make(theme,data):
    dark=theme=='dark'
    c={
      'bg':'#0A1220' if dark else '#F4F9FF',
      'card':'#132438' if dark else '#FFFFFF',
      'border':'#30435A' if dark else '#C1D8EA',
      'ink':'#F1F7FE' if dark else '#1C364C',
      'sub':'#9AB0C6' if dark else '#58738D',
      'dim':'#63829C' if dark else '#8AA2B5',
      'cyan':'#73DCEE' if dark else '#0987A3',
      'blue':'#83B6FF' if dark else '#2369B4',
      'mint':'#83E7BA' if dark else '#228F72',
      'violet':'#C5B4FF' if dark else '#7956C4',
      'empty':'#263A4D' if dark else '#E6F0F7',
    }
    components=[]
    components.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 434" width="1200" height="434" role="img" aria-labelledby="title desc">')
    components.append(f'<title id="title">Hassan — public GitHub activity</title><desc id="desc">Automatically generated metrics from the public GitHub REST API. A timeline of public events, not a complete contributions history.</desc>')
    components.append(rect(1,1,1198,432,18,c['bg'],c['border']))
    components.append(tx(44,53,'PUBLIC ACTIVITY / HSHS-DEV',c['cyan'],15,700,family='Consolas,monospace',extra='letter-spacing="1.5"'))
    components.append(tx(1156,53,'AUTOMATED · DAILY SYNC',c['sub'],13,400,'end','Consolas,monospace'))
    tiles=[('PUBLIC REPOS',data.get('repos','—'),c['cyan']),('PUBLIC STARS',data.get('stars','—'),c['blue']),('FOLLOWERS',data.get('followers','—'),c['violet']),('REPOS PUSHED · 30D',data.get('pushed','—'),c['mint'])]
    for i,(label,num,color) in enumerate(tiles):
        x=43+i*282
        components.append(rect(x,78,267,94,11,c['card'],c['border']))
        components.append(rect(x+17,95,4,21,2,color))
        components.append(tx(x+31,111,label,c['sub'],12,500,family='Consolas,monospace',extra='letter-spacing=".5"'))
        components.append(tx(x+20,152,num,c['ink'],34,700))
    # Chart is a 28-day public event heat strip. Not a calendar of commits.
    components.append(rect(43,190,1113,191,11,c['card'],c['border']))
    components.append(tx(66,222,'PUBLIC EVENTS · LAST 28 DAYS',c['ink'],17,700))
    components.append(tx(1136,222,'EVENTS ≠ COMMITS',c['dim'],12,400,'end','Consolas,monospace'))
    now=datetime.now(timezone.utc).date()
    dates=[(now-timedelta(days=i)) for i in range(27,-1,-1)]
    vals=[data.get('events',{}).get(d.isoformat(),0) for d in dates]
    maxv=max(vals or [0])
    for i,(dt,val) in enumerate(zip(dates,vals)):
        x=68+i*37.6
        # every bar has a visible baseline so the chart never collapses when counts are low
        if data.get('pending'):
            h=5+(i%5)*3
            color=c['empty']
        else:
            h=8 if maxv==0 else max(8, round(93*val/maxv))
            color=c['empty'] if val==0 else ([c['mint'],c['cyan'],c['blue']][min(2, int(val/max(1,maxv)*3))])
        components.append(rect(round(x,2),333-h,25,round(h,2),4,color))
    components.append(tx(68,355,'-28D',c['dim'],12,400,family='Consolas,monospace'))
    components.append(tx(1116,355,'TODAY (UTC)',c['dim'],12,400,'end','Consolas,monospace'))
    label=('First sync pending · run the GitHub workflow' if data.get('pending') else 'Recent public events only; GitHub does not provide a complete event history')
    components.append(tx(65,407,label,c['sub'],13))
    components.append(tx(1143,407,data.get('refreshed','Not synced yet'),c['dim'],12,400,'end','Consolas,monospace'))
    components.append('</svg>')
    return '\n'.join(components)

def main():
    if '--placeholder' in sys.argv:
        data={'repos':'—','stars':'—','followers':'—','pushed':'—','events':{},'refreshed':'WAITING FOR FIRST SYNC','pending':True}
    else:
        try: data=collect()
        except (HTTPError,URLError,TimeoutError,ValueError,KeyError) as err:
            # Fail workflow without overwriting last-known-good assets.
            print(f'Unable to load public GitHub API data: {err}', file=sys.stderr)
            return 1
    for theme in ('dark','light'):
        (OUT/f'activity.{theme}.svg').write_text(make(theme,data),encoding='utf-8')
    print(f"Generated activity cards ({'placeholder' if data['pending'] else 'live data'})")
    return 0

if __name__=='__main__': sys.exit(main())
