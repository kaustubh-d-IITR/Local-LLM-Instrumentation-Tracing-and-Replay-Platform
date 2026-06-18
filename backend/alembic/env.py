from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config import settings
from app.models.base import Base
# Explicitly import all models to ensure they register with Base.metadata
import app.models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

import logging
from urllib.parse import urlparse

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# Resolve the database URL
db_url = settings.SQLALCHEMY_DATABASE_URI
if not db_url:
    import os
    db_url = os.getenv("DATABASE_URL", "").replace("postgres://", "postgresql://", 1)

# Log the resolved host to ensure we aren't defaulting to localhost in production
parsed_url = urlparse(db_url)
logger = logging.getLogger("alembic.env")
logger.info(f"Alembic successfully resolved connection string. Host target: {parsed_url.hostname}")

# Print all discovered tables from Base.metadata to prove models are registered
discovered_tables = list(Base.metadata.tables.keys())
logger.info(f"Discovered tables in Base.metadata: {discovered_tables}")

# overwrite sqlalchemy.url
config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            # Add requested startup logging
            current_rev = context.get_context().get_current_revision()
            head_rev = context.get_head_revision()
            logger.info(f"Current Alembic revision: {current_rev}")
            logger.info(f"Target Alembic revision: {head_rev}")
            
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
