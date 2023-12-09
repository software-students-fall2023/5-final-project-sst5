document.addEventListener("DOMContentLoaded", function () {
  var guessForm = document.getElementById("guessForm");

  var answerElement = document.getElementById("answer");
  var answer = answerElement.dataset.answer;

  guessForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var pokemonGuess = document.getElementById("guessPokemon").value;

    fetch("compare", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: pokemonGuess, answer: answer }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});
