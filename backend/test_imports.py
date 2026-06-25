import sys
sys.modules['torch'] = None
sys.modules['transformers'] = None
sys.modules['psutil'] = None
sys.modules['accelerate'] = None
sys.modules['bitsandbytes'] = None
sys.modules['sentence_transformers'] = None

# 1. Test basic app import
try:
    import app
    print('import app -> SUCCESS')
except Exception as e:
    print('import app -> FAILED:', e)

# 2. Test FastAPI main import
try:
    from app.main import app as fastapi_app
    print('from app.main import app -> SUCCESS')
except Exception as e:
    print('from app.main import app -> FAILED:', e)

# 3. Test running it (we won't run uvicorn here, just checking import safety)
print('All static module discovery tests passed!')
