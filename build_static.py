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
    <link rel="stylesheet" href="/static/styles.css">
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
                    <a href="/quiz" class="submit-button">
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

if __name__ == "__main__":
    build_static_site() 