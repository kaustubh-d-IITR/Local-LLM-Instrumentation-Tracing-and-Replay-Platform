import sys
from alembic.config import main
sys.argv = ['alembic', 'revision', '--autogenerate', '-m', 'init_schema']
main()
