"""
Web app for the face recognition project.
"""
import os
import sys
import requests
import random

current_script_path = os.path.abspath(__file__)

project_path = os.path.dirname(os.path.dirname(current_script_path))

sys.path.append(project_path)

from db import db

from flask import Flask, render_template, request, jsonify, session, url_for, redirect

current_script_path = os.path.abspath(__file__)

project_path = os.path.dirname(os.path.dirname(current_script_path))

sys.path.append(project_path)

from pymongo import MongoClient  # pylint: disable=wrong-import-position
from dotenv import load_dotenv  # pylint: disable=wrong-import-position

load_dotenv()

# MONGO_URI = "mongodb://mongodb:27017/"

# # Connect to MongoDB
# client = MongoClient(MONGO_URI)

app = Flask(__name__)
app.secret_key = 'secret_key'

print(db)

pokemonCollection = db["pokemon"]


@app.route("/")  # Route for /
def index():
    """Returns index page."""

    message = session.pop('message', None)
    return render_template('index.html', message=message)

@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.form.get('username')
    session['username'] = username
    session['message'] = "Username successfully saved! It will be used for the leaderboards"
    return redirect(url_for('index'))

@app.route("/game")  # Route for /game
def game():
    """Returns game page."""

    total_documents = pokemonCollection.count_documents({})

    random_index = random.randint(0, total_documents - 1)

    random_document = pokemonCollection.aggregate([
        {"$skip": random_index},
        {"$limit": 1}
    ])
    entry = next(random_document, None)

    return render_template("game.html", answer=entry["Pokemon"])

@app.route("/compare", methods=["POST"])  # Route for /compare
def compare():
    """Returns comparing page."""
    data = request.get_json()
    pokemonGuess = data["name"].capitalize()

    answer_data = poke_find_data = pokemonCollection.find_one({"Pokemon": data["answer"]})

    poke_find_data = pokemonCollection.find_one({"Pokemon": pokemonGuess})

    print(answer_data)

    if(poke_find_data is None):
        return jsonify({"msg": "No pokemon with this name was found, please try again"})
    else:
        typeOne = True if poke_find_data["Type I"] == answer_data["Type I"] else False
        typeTwo = True if poke_find_data["Type II"] == answer_data["Type II"] else False
        tier = True if poke_find_data["Tier"] == answer_data["Tier"] else False
        egOne = True if poke_find_data["Egg Group I"] == answer_data["Egg Group I"] else False
        egTwo = True if poke_find_data["Egg Group II"] == answer_data["Egg Group II"] else False
        generation = True if poke_find_data["generation"] == answer_data["generation"] else False

        evoStatusOne = True if (poke_find_data["Evolve"] != 'N' and poke_find_data["Evolve"] != '') else False
        evoStatusTwo = True if (answer_data["Evolve"] != 'N' and answer_data["Evolve"] != '') else False

        isEvo = True if (evoStatusOne == evoStatusTwo) else False #??????
        return jsonify({"msg": "Pokemon found successfully", "typeOne" : typeOne, "typeTwo" : typeTwo, "tier": tier, "egOne":egOne, "egTwo": egTwo, "generation" :generation, "isEvo": isEvo})
    
@app.route("/scoreboard")
def scoreboard():
    """Returns scoreboard page."""

    scoreboard_data = pokemonCollection.find(
        {"Best guesser": {"$exists": True}, "lowest guesses": {"$exists": True}},
        {"_id": 0, "Pokemon": 1, "Best guesser": 1, "lowest guesses": 1}
    )
    scoreboard_list = list(scoreboard_data)

    return render_template("scoreboard.html", scoreboard=scoreboard_list)

@app.route("/dictionary")
def dictionary():
    """Returns dictionary page."""

    cursor = pokemonCollection.find({})
    pokemon_names = [pokemon["Pokemon"] for pokemon in cursor]
    return render_template('dictionary.html', names=pokemon_names)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
