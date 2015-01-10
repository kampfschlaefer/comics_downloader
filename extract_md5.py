import json
import re

comics = json.load(open('comics_dynamite.json', 'r'))

comics = comics['subproducts']

for c in comics[:10]:
    #print c['machine_name']
    for d in c['downloads']:
        for s in d['download_struct']:
            #print d['machine_name'], s['name'], s['md5'], re.findall('.+net/([^?]+)\?', s['url']['web'])[0]
            print s['md5'], re.findall('.+net/([^?]+)\?', s['url']['web'])[0], s['url']['web']
