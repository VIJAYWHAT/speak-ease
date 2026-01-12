document.addEventListener("DOMContentLoaded", () => {
  const quizPopup = document.getElementById("quiz-popup");
  const resultPopup = document.getElementById("result-popup");
  const quizQuestion = document.getElementById("quiz-question");
  const quizOptions = document.getElementById("quiz-options");
  const resultMessage = document.getElementById("result-message");
  const openQuiz = document.getElementById("open-quiz");
  const closeQuiz = document.getElementById("close-quiz");
  const submitAnswer = document.getElementById("submit-answer");

  let selectedOption = null;
  let correctAnswer = "";
  let resultTimeoutId = null;

  function closeResultAndQuiz() {
    if (resultTimeoutId) clearTimeout(resultTimeoutId);
    resultTimeoutId = null;
    resultPopup.style.display = "none";
    quizPopup.style.display = "none";
    document.removeEventListener("click", handleResultOutsideClick);
  }

  function handleResultOutsideClick(e) {
    if (resultPopup.style.display !== "block") return;
    const content = resultPopup.querySelector(".result-content");
    if (content && content.contains(e.target)) return; // click on the message box – don't close
    closeResultAndQuiz();
  }

  // Close result when clicking outside (works for both overlay and centered box)
  function setupResultClickOutside() {
    document.removeEventListener("click", handleResultOutsideClick);
    setTimeout(
      () => document.addEventListener("click", handleResultOutsideClick),
      0
    );
  }

  // Open Quiz Popup
  openQuiz.addEventListener("click", async () => {
    quizPopup.style.display = "block";
    quizOptions.innerHTML = "Loading...";

    try {
      const response = await fetch("/get_quiz");
      const data = await response.json();

      if (data.error) {
        quizQuestion.textContent = "No Quiz Available!";
        quizOptions.innerHTML = "";
        return;
      }

      // Set question and options
      quizQuestion.textContent = data.question;
      correctAnswer = data.correct_answer;

      quizOptions.innerHTML = "";
      data.options.forEach((option, index) => {
        const optionButton = document.createElement("button");
        optionButton.textContent = option;
        optionButton.classList.add("quiz-option");
        optionButton.dataset.value = `option${index + 1}`;

        optionButton.addEventListener("click", () => {
          selectedOption = optionButton.dataset.value;
          document
            .querySelectorAll(".quiz-option")
            .forEach((btn) => (btn.style.background = ""));
          optionButton.style.background = "#28a745"; // Highlight selected option
        });

        quizOptions.appendChild(optionButton);
      });
    } catch (error) {
      quizQuestion.textContent = "Error loading quiz!";
      quizOptions.innerHTML = "";
    }
  });

  // Close Quiz Popup
  closeQuiz.addEventListener("click", () => {
    quizPopup.style.display = "none";
  });

  // Submit Answer
  submitAnswer.addEventListener("click", () => {
    if (!selectedOption) {
      alert("Please select an answer!");
      return;
    }

    if (correctAnswer.includes(selectedOption)) {
      showResultPopup("🎉 Congrats! Correct Answer", true);
    } else {
      showResultPopup("❌ Wrong Answer", false);
    }
  });

  // Show Result Popup
  function showResultPopup(message, isCorrect) {
    resultMessage.textContent = message;
    resultMessage.style.color = isCorrect ? "green" : "red";
    resultPopup.style.display = "block";

    if (resultTimeoutId) clearTimeout(resultTimeoutId);
    resultTimeoutId = setTimeout(closeResultAndQuiz, 2000);
    setupResultClickOutside();
  }
});
