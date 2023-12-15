"""
Web app for the face recognition project.
"""
import os
import sys
import requests
import random

# current_script_path = os.path.abspath(__file__)

# project_path = os.path.dirname(os.path.dirname(current_script_path))

# sys.path.append(project_path)

# from db import db

from flask import Flask, render_template, request, jsonify, session, url_for, redirect

# current_script_path = os.path.abspath(__file__)

# project_path = os.path.dirname(os.path.dirname(current_script_path))

# sys.path.append(project_path)

from pymongo import MongoClient  # pylint: disable=wrong-import-position
from dotenv import load_dotenv  # pylint: disable=wrong-import-position

load_dotenv()

# MONGO_URI = "mongodb://mongodb:27017/"

# # Connect to MongoDB
# client = MongoClient(MONGO_URI)

app = Flask(__name__)
app.secret_key = 'secret_key'

# print(db)

# pokemonCollection = db["pokemon"]

client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
pokemonCollection = database[os.getenv("MONGODB_COLLECTION", "pokemon")]
leaderboardCollection = database["leaderboard"]


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

    answer_data = pokemonCollection.find_one({"Pokemon": data["answer"]})
    poke_find_data = pokemonCollection.find_one({"Pokemon": pokemonGuess})

    if(poke_find_data is None):
        return jsonify({"msg": "No pokemon with this name was found, please try again"})
    else:
        # Check type, gives partial correctness for switching primary and secondary types.
        isTypeOne = 1 if poke_find_data["Type I"] == answer_data["Type I"] else 0
        isTypeTwo = 1 if poke_find_data["Type II"] == answer_data["Type II"] else 0
        isTypeOne = 0.5 if poke_find_data["Type I"] == answer_data["Type II"] else isTypeOne
        isTypeTwo = 0.5 if poke_find_data["Type II"] == answer_data["Type I"] else isTypeTwo

        isTier = 1 if poke_find_data["Tier"] == answer_data["Tier"] else 0

        # Check egg group, gives partial correctness for switching primary and secondary egg groups.
        isEgOne = 1 if poke_find_data["Egg Group I"] == answer_data["Egg Group I"] else 0
        isEgTwo = 1 if poke_find_data["Egg Group II"] == answer_data["Egg Group II"] else 0
        isEgOne = 0.5 if poke_find_data["Egg Group I"] == answer_data["Egg Group II"] else isEgOne
        isEgTwo = 0.5 if poke_find_data["Egg Group II"] == answer_data["Egg Group I"] else isEgTwo

        isGeneration = 1 if poke_find_data["generation"] == answer_data["generation"] else 0

        # Checks evolution, treats N and Blank as the same. Treats Lv. evolutions as the same.
        evoStatusOne = poke_find_data["Evolve"] if (poke_find_data["Evolve"] != 'N' and poke_find_data["Evolve"] != '') else ''
        evoStatusTwo = answer_data["Evolve"] if (answer_data["Evolve"] != 'N' and answer_data["Evolve"] != '') else ''
        evoStatusOne = 'Evolution' if evoStatusOne.split('.')[0] == 'Lv' else evoStatusOne
        evoStatusTwo = 'Evolution' if evoStatusTwo.split('.')[0] == 'Lv' else evoStatusTwo

        isEvo = 1 if (evoStatusOne == evoStatusTwo) else 0  # ??????
        evolution = evoStatusOne

        isPokemon = 1 if (pokemonGuess == data["answer"]) else 0
        return jsonify({"msg": "Pokemon found successfully", "Pokemon":pokemonGuess, "TypeOne": poke_find_data["Type I"],
                        "TypeTwo": poke_find_data["Type II"], "Tier": poke_find_data["Tier"],
                        "EgOne": poke_find_data["Egg Group I"], "EgTwo": poke_find_data["Egg Group II"],
                        "Generation": poke_find_data["generation"], "Evo": evolution, "isEvo": isEvo,
                        "isTypeOne": isTypeOne, "isTypeTwo": isTypeTwo, "isTier": isTier, "isEgOne": isEgOne,
                        "isEgTwo": isEgTwo, "isGeneration": isGeneration, "isPokemon":isPokemon})
    
@app.route("/update_leaderboard", methods=["POST"])
def update_leaderboard():
    data = request.get_json()
    pokemon_name = data["pokemon"]
    guesses = data["guesses"]
    # print(guesses)
    username = session.get("username")

    if not username:
        username = "Anonymous User"

    # current_record = find_record(pokemon_name)
    if check_if_new_record(pokemon_name, guesses):
        leaderboardCollection.update_one(
            {"Pokemon": pokemon_name},
            {"$set": {"Best guesser": username, "Lowest guesses": guesses}},
            upsert=True
        )
        return jsonify({"success": "Leaderboard updated successfully"})
    else:
        return jsonify({"success": "Current guess not a record"})
def check_if_new_record(pokemon_name, guesses):
    current_record = leaderboardCollection.find_one(
        {"Pokemon": pokemon_name},
        {"_id": 0, "Best guesser": 1, "Lowest guesses": 1}
    )
    return current_record is None or guesses < current_record.get("Lowest guesses", float('inf'))
  
@app.route("/scoreboard")
def scoreboard():
    """Returns scoreboard page."""

    scoreboard_data = leaderboardCollection.find(
        {},
        {"_id": 0, "Pokemon": 1, "Best guesser": 1, "Lowest guesses": 1}
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
