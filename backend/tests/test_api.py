from fastapi.testclient import TestClient
from backend.app.main import create_app
import pytest

@pytest.fixture
def client(tmp_path):
    app=create_app(f"sqlite:///{tmp_path / 'test.db'}")
    with TestClient(app) as c: yield c
    app.state.engine.dispose()

def test_health_and_reset(client):
    assert client.get('/api/health').json()['externalServices'] is False
    original=client.get('/api/state').json()
    reset=client.post('/api/reset',json={'expected_revision':original['revision']})
    assert reset.status_code==200
    assert reset.json()['data']==original['data']
    assert reset.json()['revision']==original['revision']+1

def test_stale_revision_rejected_without_lost_write(client):
    client.post('/api/reset',json={'expected_revision':0})
    assert client.post('/api/reset',json={'expected_revision':0}).status_code==409
    assert client.get('/api/state').json()['revision']==1

def test_export_is_downloadable_json(client):
    response=client.get('/api/export')
    assert response.status_code==200 and response.json()['mode']=='demo'
    assert 'attachment' in response.headers['content-disposition']

def test_analyze_is_evidence_linked_and_persistent(client):
    response=client.post('/api/conversations/CALL-021/analyze',json={'expected_revision':0})
    assert response.status_code==200
    c=response.json()['data']['conversations'][20]
    assert c['analysis']['modelVersion']=='deterministic-demo-v1'
    assert client.get('/api/state').json()['data']['conversations'][20]['analysis']==c['analysis']
    assert client.post('/api/conversations/UNKNOWN/analyze',json={}).status_code==404

def test_reset_preserves_audio_metadata(client):
    state=client.post('/api/reset',json={}).json()['data']
    assert len(state['conversations'])==30
    assert sum(bool(c['audio']) for c in state['conversations'])==5

