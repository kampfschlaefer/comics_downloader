
from comic_downloader import informationextractor


def test_parse_json():
    data = informationextractor.parse_comics_json('tests/demo_comics.json')
    assert data.keys() == [
        'pdfquality_warning_comics',
        'imageexpo2015_previewbook',
        'alexandada_vol1'
    ]
    assert sorted(data['alexandada_vol1'].keys()) == [
        'CBZ', 'EPUB', 'PDF', 'PDF (HQ)'
    ]


# def test_produce_epub_md5():
#     assert 0
