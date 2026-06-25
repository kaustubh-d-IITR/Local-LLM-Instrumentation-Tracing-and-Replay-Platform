import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.token import Token
from app.models.session import Session as SessionModel
import uuid

Base.metadata.create_all(bind=engine)

def insert_test_token():
    db = SessionLocal()
    session_id = str(uuid.uuid4())
    db.add(SessionModel(id=session_id, model_name="gpt2", prompt="test"))
    db.commit()
    db.add(Token(session_id=session_id, idx=0, token="test_token_1", ms=1.0))
    db.add(Token(session_id=session_id, idx=1, token="test_token_2", ms=2.0))
    db.commit()
    return session_id

session_id = insert_test_token()
print(f'Inserted test token for session: {session_id}')

import uvicorn
import threading
import time
import requests
from app.main import app

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8009, log_level='warning')

t = threading.Thread(target=run_server, daemon=True)
t.start()

import socket
def wait_for_port(port, host='127.0.0.1', timeout=15.0):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except OSError:
            time.sleep(0.5)
            if time.time() - start_time >= timeout:
                return False

print('Waiting for server...')
if not wait_for_port(8009):
    print('Server did not start in time')
    sys.exit(1)
print('Server started!')
try:
    response = requests.get(f'http://127.0.0.1:8009/sessions/{session_id}/tokens')
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(e)
