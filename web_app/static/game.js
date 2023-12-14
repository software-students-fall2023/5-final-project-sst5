let guesses = 0;

document.addEventListener("DOMContentLoaded", function () {
  var guessForm = document.getElementById("guessForm");

  var answerElement = document.getElementById("answer");
  var answer = answerElement.dataset.answer;

  guessForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var pokemonGuess = $('#guessPokemon').val();
    let correctness;

    fetch("compare", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: pokemonGuess, answer: answer }),
    })
      .then((response) => response.json())
      .then((data) => {
          $('#feedback-text').text(data['msg']);
          if(data['Pokemon']){
              guesses++;
              correctness = getCorrectness(data);
              comparisons.addGuess(data, correctness);
              if(checkWin(correctness)){
                  $('#feedback-text').text("You guessed it!");
                  updateLeaderboard(answer, guesses);
                  $('.win').show();
              }
              $('#guessPokemon').val('');
          }
          console.log(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});

function updateLeaderboard(pokemonName, guesses) {
  fetch("/update_leaderboard", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          pokemon: pokemonName,
          guesses: guesses
      }),
  })
  .then((response) => response.json())
  .then((data) => {
      console.log("Leaderboard updated:", data);
  })
  .catch((error) => {
      console.error("Error updating leaderboard:", error);
  });
}
