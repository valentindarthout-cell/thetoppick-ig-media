import sys,os,json
sys.path.insert(0,'/home/claude/thetoppick-ig-media/tools')
from engine import *
from posts_week2_example import POSTS
OUT='/home/claude/thetoppick-ig-media/posts'
only=sys.argv[1:]
for p in POSTS:
    if only and p['code'] not in only: continue
    os.makedirs(f"{OUT}/{p['code']}",exist_ok=True)
    n=len(p['slides'])
    for i,s in enumerate(p['slides']):
        k=kinds_for(p['pillar'],i,n,s)
        y=render(s,k,i+1,n,f"{OUT}/{p['code']}/{p['code']}-{i+1:02d}.jpg",closing=(i==n-1))
        print(p['code'],i+1,y)
