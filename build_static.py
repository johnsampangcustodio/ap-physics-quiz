import os
import shutil
from pathlib import Path

def build_static_site():
    # Create static_site directory
    static_dir = Path("static_site")
    if static_dir.exists():
        shutil.rmtree(static_dir)
    static_dir.mkdir()

    # Copy static files
    shutil.copytree("ap_physics_quiz/static", static_dir / "static")
    shutil.copytree("ap_physics_quiz/templates", static_dir / "templates")

    # Create index.html
    with open(static_dir / "index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AP Physics C Mechanics Quiz</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="./static/styles.css">
    <style>
        body {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        main {
            flex: 1;
        }
    </style>
</head>
<body>
    <div class="forest-decoration"></div>
    <header class="p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold text-white">AP Physics C Mechanics Quiz 🌲</h1>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        <div class="question-card">
            <div class="kawaii-element" style="top: 10%; left: 5%;">🌿</div>
            <div class="kawaii-element" style="top: 20%; right: 5%;">🌸</div>
            <div class="kawaii-element" style="bottom: 10%; left: 10%;">🍄</div>
            
            <div class="text-center">
                <h2 class="text-3xl font-bold text-forest-green mb-4">Welcome to the AP Physics C Mechanics Quiz!</h2>
                <p class="text-lg text-gray-700 mb-6">
                    Test your knowledge of AP Physics C Mechanics with random questions. 
                    Try to answer correctly to increase your score!
                </p>
                
                <div class="mt-8">
                    <a href="./quiz.html" class="submit-button">
                        Start Quiz 🌱
                    </a>
                </div>
            </div>
        </div>
    </main>

    <footer class="p-4 mt-auto">
        <div class="container mx-auto text-center">
            <p>&copy; 2025 AP Physics C Mechanics Quiz 🌳</p>
        </div>
    </footer>
</body>
</html>""")

    # Create quiz.html
    with open(static_dir / "quiz.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AP Physics C Mechanics Quiz</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="./static/styles.css">
    <style>
        body {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        main {
            flex: 1;
        }
    </style>
</head>
<body>
    <div class="forest-decoration"></div>
    <header class="p-4">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold text-white">AP Physics C Mechanics Quiz 🌲</h1>
            <div class="score-display">
                Score: <span id="score">0</span> 🌟
                <div class="progress-bar">
                    <div class="progress-fill" id="progress"></div>
                </div>
            </div>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        <div class="question-card">
            <div class="kawaii-element" style="top: 10%; left: 5%;">🌿</div>
            <div class="kawaii-element" style="top: 20%; right: 5%;">🌸</div>
            <div class="kawaii-element" style="bottom: 10%; left: 10%;">🍄</div>
            
            <div id="question-container">
                <h2 class="text-2xl font-bold text-forest-green mb-4">Question:</h2>
                <p class="text-lg text-gray-700 mb-6" id="question-text"></p>

                <div id="options-container" class="space-y-3 mb-6"></div>
                
                <div class="mt-8 flex justify-center">
                    <button type="button" class="submit-button" id="submit-answer">
                        Submit Answer 🌱
                    </button>
                </div>
            </div>
        </div>
    </main>

    <footer class="p-4 mt-auto">
        <div class="container mx-auto text-center">
            <p>&copy; 2025 AP Physics C Mechanics Quiz 🌳</p>
        </div>
    </footer>

    <script>
        // Sample questions (you can replace this with your actual questions)
        const questions = [
            {
                text: "A block of mass 2 kg is sliding on a frictionless surface with a velocity of 3 m/s. What is its kinetic energy?",
                options: ["3 J", "6 J", "9 J", "18 J"],
                correct: "9 J",
                explanation: "Kinetic energy is calculated using the formula KE = (1/2)mv². For a 2 kg block moving at 3 m/s, KE = 0.5 × 2 × 3² = 9 J."
            },
            {
                text: "A 5 kg object accelerates from rest to 10 m/s in 5 seconds. What is the magnitude of the net force acting on it?",
                options: ["5 N", "10 N", "15 N", "20 N"],
                correct: "10 N",
                explanation: "Using Newton's Second Law, F = ma. The acceleration is (change in velocity)/(time) = 10/5 = 2 m/s². Therefore, F = 5 kg × 2 m/s² = 10 N."
            }
        ];

        let currentQuestion = 0;
        let score = 0;

        function displayQuestion() {
            const question = questions[currentQuestion];
            document.getElementById('question-text').textContent = question.text;
            
            const optionsContainer = document.getElementById('options-container');
            optionsContainer.innerHTML = '';
            
            question.options.forEach(option => {
                const label = document.createElement('label');
                label.className = 'answer-option flex items-start';
                label.innerHTML = `
                    <input type="radio" name="answer" value="${option}" class="mt-1 mr-3" required>
                    <span>${option}</span>
                    <span class="ml-auto">👉</span>
                `;
                optionsContainer.appendChild(label);
            });
        }

        function checkAnswer() {
            const selectedAnswer = document.querySelector('input[name="answer"]:checked');
            if (!selectedAnswer) return;

            const question = questions[currentQuestion];
            const isCorrect = selectedAnswer.value === question.correct;

            if (isCorrect) {
                score++;
                document.getElementById('score').textContent = score;
                document.getElementById('progress').style.width = `${(score/questions.length)*100}%`;
            }

            // Show result
            const resultDiv = document.createElement('div');
            resultDiv.className = isCorrect ? 'bg-leaf-green text-white p-4 mb-6 rounded-lg border-2 border-tan' : 'bg-red-500 text-white p-4 mb-6 rounded-lg border-2 border-tan';
            resultDiv.innerHTML = `
                <div class="flex items-center">
                    <span class="text-2xl mr-3">${isCorrect ? '🎉' : '💫'}</span>
                    <p class="text-xl font-bold">${isCorrect ? 'Correct!' : 'Incorrect'}</p>
                </div>
                <p class="mt-2">${isCorrect ? `Your answer "${selectedAnswer.value}" is correct. +1 point! 🌟` : `Your answer "${selectedAnswer.value}" is not correct.`}</p>
                ${!isCorrect ? `
                <div class="mt-4 bg-light-green p-4 rounded-lg">
                    <p class="font-bold">The correct answer is: ${question.correct}</p>
                    <p class="mt-2">${question.explanation}</p>
                </div>
                ` : ''}
            `;

            document.getElementById('question-container').appendChild(resultDiv);

            // Disable submit button and show next question button
            document.getElementById('submit-answer').disabled = true;
            const nextButton = document.createElement('button');
            nextButton.className = 'submit-button mt-4';
            nextButton.textContent = 'Next Question 🌱';
            nextButton.onclick = () => {
                currentQuestion = (currentQuestion + 1) % questions.length;
                document.getElementById('question-container').innerHTML = '';
                displayQuestion();
                document.getElementById('submit-answer').disabled = false;
            };
            document.getElementById('question-container').appendChild(nextButton);
        }

        document.getElementById('submit-answer').onclick = checkAnswer;
        displayQuestion();
    </script>
</body>
</html>""")

if __name__ == "__main__":
    build_static_site() 