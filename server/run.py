from dotenv import load_dotenv
load_dotenv()

import os
from app import app

app.run(port=8080)

# To Run:
# python run.py
# or
# python -m flask run
