import sys
sys.modules['torch'] = None
sys.modules['transformers'] = None
import uvicorn
from app.main import app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
