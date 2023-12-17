![webapp workflow](https://github.com/software-students-fall2023/5-final-project-sst5/actions/workflows/web-app.yml/badge.svg)

# Guess That Pokemon!

Our project is Guess That Pokemon, a game where users will be given multiple attempts to guess the random pokemon that was chosen between generation 1 and generation 5. As they continue guessing pokemon they will recieve hints based on what characteristics of the pokemon they got correct and which they got wrong. If the user successfully guess the pokemon, they will be given the opportunity to store their name in the leaderboards along with how many guesses it took for them to get the correct pokemon.

# Links to container images

There are two containers. The first one is our database, and the second one is the web app.

- [pokemonmongodb](https://hub.docker.com/r/capks/pokemonmongodb)
- [guess_that_pokemon](https://hub.docker.com/r/capks/guess_that_pokemon)

# How to run

## Method 1: Accessing the site

Please go to [http://161.35.110.214:5000](http://161.35.110.214:5000) in any browser to run our game. This is currently being deployed on Digital Ocean so there is no additional setup needed. There are also no enviornmental variables or data needed for the game to run properly.

## Method 2: Docker Compose

- Step 1: Clone the repository with:
```
git clone <URL>
```
- Step 2: CD to the root of the repository
- Step 3: Ensure docker is active and do:
```
docker-compose build
docker-compose up
```
- Step 4: Access the website at http://localhost:5000/

## Method 3: Running app.py

- Step 1: Clone the repository similar to method 2.
- Step 2: Open the project in VS code
- Step 3: Download dependencies. You can do this if you CD to the root of the project and run:
```
pip install -r requirements.txt
```
- Step 4: Run app.py

# Set up

- Only method 3 requires downloading the dependencies manually.
- There is no additional setup or data import required for the system to run correctly.

# Contributors

- [Emos Ker](https://github.com/Capksz)
- [Allyson Chan](https://github.com/tinybitofheaven)
- [Ryan Zhang](https://github.com/CouriersRyan)
- [Richard Li](https://github.com/Silver1793)
