import io
import os
import pytest

from unittest.mock import Mock, patch
import mongomock
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

from web_app.app import app


@pytest.fixture
def client():
    """configuring Flask application to run in testing"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mongo():
    return mongomock.MongoClient()
  
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
    assert json_data["isEgOne"] == False
    assert json_data["isEgTwo"] == False
    assert json_data["isEvo"] == True
    assert json_data["isGeneration"] == False
    assert json_data["isPokemon"] == False
    assert json_data["isTier"] == True
    assert json_data["isTypeOne"] == False
    assert json_data["isTypeTwo"] == False
    
# test compare correct answer
def test_compare_correct_answer(client):
    response = client.post("/compare", json={
        'answer': 'Venipede', 'name': 'venipede'
    })
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data["msg"] == "Pokemon found successfully"
    assert json_data["isEgOne"] == True
    assert json_data["isEgTwo"] == True
    assert json_data["isEvo"] == True
    assert json_data["isGeneration"] == True
    assert json_data["isPokemon"] == True
    assert json_data["isTier"] == True
    assert json_data["isTypeOne"] == True
    assert json_data["isTypeTwo"] == True

# test new record
def test_update_leaderboard_new_entry(client):
    mocked_mongo = mongomock.MongoClient()
    with patch("web_app.app.check_if_new_record", return_value=True):
        response = client.post("/update_leaderboard", json={
            'pokemon': 'Venipede', 'guesses': 3, 'username': 'new-scorer'
        })
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["success"] == "Leaderboard updated successfully"

# test update record higher score
def test_update_leaderboard_higher_score(client):
    mocked_mongo = mongomock.MongoClient()
    with patch("web_app.app.check_if_new_record", return_value=False):
        response = client.post("/update_leaderboard", json={
            'pokemon': 'Venipede', 'guesses': 2, 'username': 'new-scorer'
        })
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["success"] == "Current guess not a record"
