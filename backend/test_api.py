import sys
import threading
import time
import requests
import uvicorn
from app.main import app

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8005, log_level='info')

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    # Wait for server to boot
    time.sleep(5)
    
    print('Executing POST /sessions/start...')
    try:
        response = requests.post(
            'http://127.0.0.1:8005/sessions/start',
            json={"model_name": "gpt2", "prompt": "Hello world!"}
        )
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.json()}')
    except Exception as e:
        print(f'Error hitting API: {e}')
