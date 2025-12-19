import pytest
import json
from app import app, analyze_text

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analyze_text():
    text = "hello world hello"
    total_words, top_words = analyze_text(text)
    
    assert total_words == 3 #nosec
    assert ('hello', 2) in top_words #nosec
    assert ('world', 1) in top_words #nosec

def test_analyze_endpoint(client):
    # Тест валидного запроса
    data = {'text': 'hello world hello'}
    response = client.post('/analyze', 
                          data=json.dumps(data),
                          content_type='application/json')
    
    assert response.status_code == 200 #nosec
    result = json.loads(response.data)
    assert result['total_words'] == 3 #nosec
    assert len(result['top_words']) == 2 #nosec
    
    # Тест пустого запроса
    response = client.post('/analyze', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400 #nosec

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200 #nosec
    result = json.loads(response.data)
    assert result['status'] == 'healthy' #nosec