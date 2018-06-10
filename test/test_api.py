import requests
import pytest

URL = 'http://localhost:5000'


@pytest.fixture(scope='module')
def google_id():
    r = requests.post('%s/url' % URL, json={
        'url':  'https://google.com',
        'tags': ['google'],
        })
    r.raise_for_status()
    data = r.json()
    assert data['id']
    return data['id']


@pytest.fixture(scope='module')
def custom_id():
    r = requests.post('%s/url/custom_id' % URL, json={
        'url':  'https://some-url.com',
        'tags': ['tag', 'google'],
        })
    r.raise_for_status()
    data = r.json()
    assert data['id']
    return data['id']


def test_get(google_id):
    r = requests.get('%s/url/%s' % (URL, google_id))
    r.raise_for_status()
    assert r.json() == {
            'id': google_id,
            'hits': 0,
            'destination': 'https://google.com',
            'tags': ['google'],
            }


def test_fwd(google_id):
    r = requests.get('%s/fwd/%s' % (URL, google_id))
    assert len(r.history) == 2
    assert r.history[0].is_redirect
    assert r.url == 'https://www.google.com/'

    r = requests.get('%s/url/%s' % (URL, google_id))
    r.raise_for_status()
    assert r.json() == {
            'id': google_id,
            'hits': 1,
            'destination': 'https://google.com',
            'tags': ['google'],
            }


def test_custom_id(custom_id):
    assert requests.get('%s/url/%s' % (URL, custom_id)).json() == {
            'id': custom_id,
            'hits': 0,
            'destination': 'https://some-url.com',
            'tags': ['tag', 'google'],
            }


def test_tagged_empty():
    r = requests.get('%s/tagged/non-existent' % URL)
    r.raise_for_status()
    assert [r['id'] for r in r.json()] == []


def test_tagged(google_id, custom_id):
    r = requests.get('%s/tagged/tag' % URL)
    r.raise_for_status()
    assert set(r['id'] for r in r.json()) == {custom_id}

    r = requests.get('%s/tagged/google' % URL)
    r.raise_for_status()
    assert set(r['id'] for r in r.json()) == {google_id, custom_id}


def test_delete():
    id = requests.post('%s/url' % URL, json={
        'url': 'https://abc.com',
        'tags': ['abc'],
        }).json()['id']

    r = requests.delete('%s/url/%s' % (URL, id))
    r.raise_for_status()
    urls = requests.get('%s/tagged/abc' % URL).json()
    assert urls == []

    assert requests.get('%s/url/%s' % (URL, id)).status_code == 404
    assert requests.get('%s/fwd/%s' % (URL, id)).status_code == 404
