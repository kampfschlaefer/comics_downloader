
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

        for d in c['downloads']:
            for ds in d['download_struct']:
                result[name][ds['name']] = {
                    'md5': ds['md5'],
                    'sha1': ds.get('sha1', ''),
                    'url': ds['url']['web'],
                    'targetname': os.path.join(
                        name,
                        re.findall(
                            '.+(?:net|com)/([^?]+)\?',
                            ds['url']['web']
                        )[0]
                    )
                }

    return result


def filter_filetypes(comics, filetype):
    if filetype not in ['PDFHQ', 'PDFHD', 'PDF', 'EPUB', 'CBZ']:
        raise ValueError('invalid filetype to extract: %s' % filetype)
    if filetype == 'PDFHQ':
        filetype = 'PDF (HQ)'
    if filetype == 'PDFHD':
        filetype = 'PDF (HD)'
    result = {}
    for name, c in list(comics.items()):
        try:
            result[name] = c[filetype]
        except KeyError:
            if filetype.startswith('PDF '):
                try:
                    result[name] = c['PDF']
                except KeyError:
                    pass
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
        default='md5', choices=['md5', 'sha1', 'urls', 'download']
    )
    parser.add_argument(
        '--filetype', '-f', dest='filetype',
        default='EPUB', choices=['PDFHQ', 'PDFHD', 'PDF', 'EPUB', 'CBZ']
    )

    args = parser.parse_args(cmd_args)

    comics = parse_comics_json(args.jsonfile)

    comics = filter_filetypes(comics, args.filetype)

    if args.extract in ['md5', 'sha1']:
        for name, c in list(comics.items()):
            if args.extract in c and c[args.extract] != '':
                print("%s %s" % (c[args.extract], c['targetname']))

    if args.extract == 'urls':
        for name, c in list(comics.items()):
            print(c['url'])

    if args.extract == 'download':
        for c in list(comics.values()):
            if not os.path.isdir(os.path.dirname(c['targetname'])):
                os.makedirs(os.path.dirname(c['targetname']))
            if not os.path.isfile(c['targetname']):
                subprocess.check_call([
                    # 'echo',
                    'wget', '-c',
                    '-O', c['targetname'],
                    c['url']
                ])
            else:
                print('! Skipping %s as it exists already!' % c['targetname'])

if __name__ == '__main__':  # pragma: no cover
    run()
