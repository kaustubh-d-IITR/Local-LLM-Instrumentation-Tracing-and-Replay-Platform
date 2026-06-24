import sys
import threading
import time
import subprocess
import requests
import uvicorn
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

def main():
    print("Starting FastAPI test server...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8008"],
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
    )
    
    time.sleep(10)
    
    print('Executing POST /sessions/start...')
    try:
        response = requests.post(
            'http://127.0.0.1:8008/sessions/start',
            json={"model_name": "gpt2", "prompt": "Hello world!"}
        )
        if response.status_code != 200:
            print(f"FAIL: Start session failed. {response.text}")
            sys.exit(1)
            
        session_id = response.json()['id']
        print(f"Session started successfully: {session_id}")
        
        print('Waiting 25 seconds for background generation to produce telemetry...')
        time.sleep(25)
        
        # Verify
        endpoints = ["topology", "metrics", "activations", "anomalies", "memory", "tokens"]
        all_passed = True
        
        for ep in endpoints:
            r = requests.get(f'http://127.0.0.1:8008/sessions/{session_id}/{ep}')
            if r.status_code != 200:
                print(f"FAIL: /{ep} returned {r.status_code} - {r.text}")
                all_passed = False
                continue
                
            data = r.json()
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict) and 'blocks' in data:
                count = len(data['blocks'])
            else:
                count = len(data)
                
            if count > 0:
                print(f"PASS: /{ep} returned {count} records")
            else:
                print(f"FAIL: /{ep} returned 0 records (empty dataset)")
                all_passed = False
                
        if all_passed:
            print("\n✅ ALL END-TO-END TELEMETRY TESTS PASSED")
            server_process.terminate()
            sys.exit(0)
        else:
            print("\n❌ SOME TELEMETRY TESTS FAILED")
            server_process.terminate()
            sys.exit(1)
            
    except Exception as e:
        print(f'Error hitting API: {e}')
        server_process.terminate()
        sys.exit(1)

if __name__ == '__main__':
    main()
