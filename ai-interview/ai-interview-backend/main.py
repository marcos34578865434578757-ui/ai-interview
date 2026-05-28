import os
from app.route import create_app
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

app = create_app()


def run_migrations():
    """启动时自动运行数据库迁移"""
    try:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.warning(f"Auto migration skipped: {e}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", settings.API_PORT))

    run_migrations()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1,
    )
