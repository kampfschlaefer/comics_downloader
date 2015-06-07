
import pytest
from comic_downloader import informationextractor


@pytest.fixture
def comics_json():
    return informationextractor.parse_comics_json('tests/demo_comics.json')


def test_parse_json(comics_json):
    assert list(comics_json.keys()) == [
        'pdfquality_warning_comics',
        'imageexpo2015_previewbook',
        'alexandada_vol1'
    ]
    assert sorted(comics_json['alexandada_vol1'].keys()) == [
        'CBZ', 'EPUB', 'PDF', 'PDF (HQ)'
    ]


@pytest.mark.parametrize(
    'format, ending',
    [
        ('EPUB', 'epub'),
        ('PDF', 'pdf'),
        ('CBZ', 'cbz'),
        ('PDFHQ', 'pdf'),
    ]
)
def test_filter_filetypes(comics_json, format, ending):
    filtered = informationextractor.filter_filetypes(comics_json, format)
    assert len(filtered) == 2
    for k in filtered:
        assert ending in filtered[k]['targetname']
        assert ending in filtered[k]['url']


def test_filter_filetypes_invalid_type(comics_json):
    with pytest.raises(ValueError) as e:
        informationextractor.filter_filetypes(comics_json, 'DOC')
    assert 'DOC' in str(e.value)


def test_run_without_args():
    with pytest.raises(SystemExit) as e:
        informationextractor.run([])
    assert e.value.code == 2


@pytest.mark.parametrize(
    'args, output',
    (
        (
            [],
            [
                'e7bb40aebb27b98921a338c2bee31ba4',
                'alexandada_vol1/AlexAndAda_Vol1_1420484117.epub'
            ]
        ),
        (
            ['--extract', 'sha1'],
            [
                '2eb3c68c7e1a8ddf305d0fe4ecaac993b886e6a4',
                'alexandada_vol1/AlexAndAda_Vol1_1420484117.epub'
            ]
        ),
        (
            ['--extract', 'urls'],
            [
                'http', 'gamekey',
                'AlexAndAda_Vol1_1420484117.epub'
            ]
        )
    )
)
def test_run_default_args(capsys, args, output):
    informationextractor.run(args + ['tests/demo_comics.json'])

    out, err = capsys.readouterr()
    for o in output:
        assert o in out


def test_run_download(monkeypatch):
    called_args = []
    monkeypatch.setattr(
        'subprocess.check_call',
        lambda args: called_args.append(args)
    )
    monkeypatch.setattr('os.makedirs', lambda path: None)
    informationextractor.run(
        [
            '--extract', 'download',
            '--filetype', 'PDFHQ',
            'tests/demo_comics.json'
        ]
    )
    assert len(called_args) == 2
    called_args
    destinations = set([
        'alexandada_vol1/AlexAndAda_Vol1_1420484117.pdf',
        'imageexpo2015_previewbook/ImageComicsPreviewBook2015_1420484117.pdf'
    ])
    for args in called_args:
        destinations = destinations.difference(args)
    assert destinations == set()


def test_run_download_one_existing(monkeypatch):
    monkeypatch.setattr(
        'os.path.isfile',
        lambda path: path == 'alexandada_vol1/AlexAndAda_Vol1_1420484117.pdf'
    )
    monkeypatch.setattr('os.makedirs', lambda path: None)
    called_args = []
    monkeypatch.setattr(
        'subprocess.check_call',
        lambda args: called_args.append(args)
    )
    informationextractor.run(
        [
            '--extract', 'download',
            '--filetype', 'PDFHQ',
            'tests/demo_comics.json'
        ]
    )
    assert len(called_args) == 1
