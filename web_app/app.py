"""
Web app for the face recognition project.
"""
import os
import sys
import requests

current_script_path = os.path.abspath(__file__)

project_path = os.path.dirname(os.path.dirname(current_script_path))

sys.path.append(project_path)

from db import db

from flask import Flask, render_template, request, jsonify

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

print(db)

pokemonCollection = db["pokemon"]


@app.route("/")  # Route for /
def index():
    """Returns index page."""

    return render_template("index.html")

@app.route("/game")  # Route for /game
def game():
    """Returns index page."""

    return render_template("game.html")

@app.route("/compare", methods=["POST"])  # Route for /compare
def compare():
    """Returns comparing page."""

    return render_template("compare.html")
    
@app.route("/scoreboard")
def scoreboard():
    """Returns scoreboard page."""

    return render_template("scoreboard.html")

@app.route("/dictionary")
def dictionary():
    """Returns dictionary page."""

    cursor = pokemonCollection.find({})
    pokemon_names = [pokemon["Pokemon"] for pokemon in cursor]
    return render_template('dictionary.html', names=pokemon_names)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
