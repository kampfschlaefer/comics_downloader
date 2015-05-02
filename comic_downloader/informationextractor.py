
import argparse
import json
import re
import os.path
import subprocess


def parse_comics_json(filename):
    result = {}
    data = json.load(open(filename, 'r'))
    comics = data['subproducts']
    for c in comics[:]:
        name = c['machine_name']
        if name not in result:
            result[name] = {}

        #print "Name: %s" % name
        for d in c['downloads']:
            for ds in d['download_struct']:
                #print "name: {name}, md5: {md5}, url: {url[web]}".format(**ds)
                result[name][ds['name']] = {
                    'md5': ds['md5'],
                    'url': ds['url']['web'],
                    'targetname': re.findall(
                        '.+net/([^?]+)\?',
                        ds['url']['web']
                    )[0]
                }

    return result


def filter_filetypes(comics, filetype):
    if filetype not in ['PDFHQ', 'PDF', 'EPUB', 'CBZ']:
        raise ValueError('invalid filetype to extract: %s' % filetype)
    if filetype == 'PDFHQ':
        filetype = 'PDF (HQ)'
    result = {}
    for name, c in comics.iteritems():
        if filetype in c:
            result[name] = c[filetype]
    return result


def run(cmd_args=None):
    parser = argparse.ArgumentParser(
        description='extract information from the json-files of humble bundles'
    )
    parser.add_argument(
        'jsonfile', metavar='filename', type=str, help='json-file to import'
    )
    parser.add_argument(
        '--extract', '-e', dest='extract',
        default='md5', choices=['md5', 'urls', 'download']
    )
    parser.add_argument(
        '--filetype', '-f', dest='filetype',
        default='PDFHQ', choices=['PDFHQ', 'PDF', 'EPUB', 'CBZ']
    )

    args = parser.parse_args(cmd_args)

    #print args

    comics = parse_comics_json(args.jsonfile)
    #print "comics: %s" % comics

    comics = filter_filetypes(comics, args.filetype)

    #print "selected types: %s" % comics

    if args.extract == 'md5':
        for name, c in comics.iteritems():
            print "%s %s" % (
                c['md5'],
                re.findall('.+net/([^?]+)\?', c['url'])[0]
            )

    if args.extract == 'urls':
        for name, c in comics.iteritems():
            print c['url']

    if args.extract == 'download':
        for c in comics.itervalues():
            if not os.path.isfile(c['targetname']):
                subprocess.check_call([
                    #'echo',
                    'wget', '-c',
                    '-O', c['targetname'],
                    c['url']
                ])
            else:
                print '! Skipping %s as it exists already!' % c['targetname']

if __name__ == '__main__':  # pragma: no cover
    run()
