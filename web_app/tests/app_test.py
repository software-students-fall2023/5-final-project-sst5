import io
import os
import pytest

from unittest.mock import Mock, patch
from web_app.app import app

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def client():
    """configuring Flask application to run in testing"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
def test_index_template(client):
    response = client.get("/")
    assert response.status_code == 200
    
    
def test_game_template(client):
    response = client.get("/game")
    assert response.status_code == 200

def test_scoreboard_template(client):
    response = client.get("/scoreboard")
    assert response.status_code == 200
    
def test_dictionary_template(client):
    response = client.get("/dictionary")
    assert response.status_code == 200

# test store username
def test_store_username(client):
    with patch("web_app.app.session", dict()) as session: 
        response = client.post("/set_username", data={"username": "test"})
        assert session.get("username") == "test"
        assert session.get("message") == "Username successfully saved! It will be used for the leaderboards"
    assert response.status_code == 302

# test compare invalid answer
def test_compare_invalid_answer(client):
    response = client.post("/compare", json={
        'answer': 'Venipede', 'name': 'asfd'
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data == {"msg": "No pokemon with this name was found, please try again"}
    
# test compare wrong answer
def test_compare_wrong_answer(client):
    response = client.post("/compare", json={
        'answer': 'Venipede', 'name': 'squirtle'
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["msg"] == "Pokemon found successfully"
    # more checks here
    
# test compare correct answer
def test_compare_correct_answer(client):
    response = client.post("/compare", json={
        'answer': 'Venipede', 'name': 'venipede'
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["msg"] == "Pokemon found successfully"
    # more checks here

# test update leaderboard