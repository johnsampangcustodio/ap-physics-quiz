# AP Physics C Mechanics Quiz

A web application that allows users to test their knowledge of AP Physics C Mechanics with randomly selected multiple-choice questions.

## Features

- Random AP Physics C Mechanics questions
- Multiple-choice answer options
- Score tracking
- Detailed explanations for correct answers
- Responsive design using TailwindCSS

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: TailwindCSS with Jinja2 templating
- **Database**: SQLite with SQLAlchemy ORM

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ap_physics_quiz
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Project Structure

```
ap_physics_quiz/
├── app/
│   ├── database.py     # Database models and connection
│   ├── models.py       # Pydantic models for API
├── static/             # Static assets (CSS, JS)
├── templates/          # HTML templates
│   ├── base.html       # Base template with layout
│   ├── home.html       # Homepage template
│   ├── quiz.html       # Quiz question template
│   ├── result.html     # Result page template
│   └── error.html      # Error page template
├── main.py             # FastAPI application
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## API Endpoints

- `GET /` - Homepage
- `GET /quiz` - Get a random question
- `POST /submit` - Submit an answer
- `POST /reset` - Reset the quiz score

### API (JSON) Endpoints

- `GET /api/question` - Get a random question (JSON)
- `POST /api/answer` - Submit an answer (JSON)
- `GET /api/score` - Get the current score
- `POST /api/restart` - Reset the quiz

## License

[MIT License](LICENSE) 