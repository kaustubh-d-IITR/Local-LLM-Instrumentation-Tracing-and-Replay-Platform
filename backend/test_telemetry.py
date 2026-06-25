import sys
import threading
import time
import requests
import uvicorn
from app.main import app

def run_server():
    uvicorn.run(app, host='127.0.0.1', port=8006, log_level='info')

if __name__ == '__main__':
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    
    time.sleep(5)
    
    print('Executing POST /sessions/start...')
    try:
        response = requests.post(
            'http://127.0.0.1:8006/sessions/start',
            json={"model_name": "gpt2", "prompt": "Hello world!"}
        )
        print(f'Start Response: {response.json()}')
        if 'id' not in response.json():
            print("Failed to start session")
            sys.exit(1)
        session_id = response.json()['id']
        
        print('Waiting 15 seconds for background generation to produce telemetry...')
        time.sleep(15)
        
        topology = requests.get(f'http://127.0.0.1:8006/sessions/{session_id}/topology')
        print(f'Topology: {topology.json()}')
        
        metrics = requests.get(f'http://127.0.0.1:8006/sessions/{session_id}/metrics')
        print(f'Metrics: {metrics.json()[:2]}') # print just first two
        
        tokens = requests.get(f'http://127.0.0.1:8006/sessions/{session_id}/tokens')
        print(f'Tokens: {tokens.json()[:2]}')
        
    except Exception as e:
        print(f'Error hitting API: {e}')
