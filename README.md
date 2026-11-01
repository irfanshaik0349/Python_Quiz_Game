# Python Interview Quiz Game
A responsive Flask quiz for students, with 500 questions, topic/difficulty filters, randomized quizzes, instant explanations and scores.

## Run locally
`py -m venv .venv`
`.venv\\Scripts\\activate`
`pip install -r requirements.txt`
`py app.py`
Open http://127.0.0.1:5000

## Render deployment
Build command: `pip install -r requirements.txt`
Start command: `gunicorn app:app`
