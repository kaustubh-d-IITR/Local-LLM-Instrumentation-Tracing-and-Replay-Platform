import sys
sys.modules['torch'] = None
sys.modules['transformers'] = None
sys.modules['psutil'] = None
sys.modules['accelerate'] = None
sys.modules['bitsandbytes'] = None
sys.modules['sentence_transformers'] = None

import uvicorn
from app.main import app

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8002)
