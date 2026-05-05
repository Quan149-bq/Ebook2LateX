from logging.config import fileConfig
import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
from os.path import abspath, dirname

# 1. Tải biến môi trường
load_dotenv()

# 2. Thêm thư mục backend vào sys.path để tìm thấy gói 'app'
# Đoạn này giúp Alembic hiểu đường dẫn khi chạy lệnh từ Terminal
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# 3. Import Base (Xử lý để IDE không báo lỗi gạch đỏ)
try:
    from app.models import Base
except ImportError:
    from models import Base

target_metadata = Base.metadata

# 4. Cấu hình Alembic
config = context.config

# Tự động lấy URL từ .env (Giúp bạn không phải sửa alembic.ini thủ công)
if os.getenv("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline() -> None:
    """Chạy migration ở chế độ 'offline'."""
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
    """Chạy migration ở chế độ 'online'."""
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
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()