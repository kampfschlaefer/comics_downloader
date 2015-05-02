
import pytest
from comic_downloader import informationextractor


@pytest.fixture
def comics_json():
    return informationextractor.parse_comics_json('tests/demo_comics.json')


def test_parse_json(comics_json):
    assert comics_json.keys() == [
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
                '2ef61f1e7b64b69531926ed8a7e0ed75',
                'AlexAndAda_Vol1_1420484117.pdf'
            ]
        ),
        (
            ['--extract', 'urls'],
            [
                'http', 'gamekey',
                'AlexAndAda_Vol1_1420484117.pdf'
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
    informationextractor.run(
        ['--extract', 'download', 'tests/demo_comics.json']
    )
    assert len(called_args) == 2


def test_run_download_one_existing(monkeypatch):
    monkeypatch.setattr(
        'os.path.isfile',
        lambda path: path == 'AlexAndAda_Vol1_1420484117.pdf'
    )
    called_args = []
    monkeypatch.setattr(
        'subprocess.check_call',
        lambda args: called_args.append(args)
    )
    informationextractor.run(
        ['--extract', 'download', 'tests/demo_comics.json']
    )
    assert len(called_args) == 1
