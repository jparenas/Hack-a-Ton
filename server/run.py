from dotenv import load_dotenv
load_dotenv()

import os
from app import app

app.run(host='0.0.0.0', port=os.getenv('PORT', 8080))

# To Run:
# python run.py
# or
# python -m flask run
