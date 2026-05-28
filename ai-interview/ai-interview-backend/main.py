import os
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def create_tables():
    """启动时同步创建所有数据库表（不依赖 alembic）"""
    try:
        from sqlalchemy import create_engine, text
        from app.db.models import Base
        import app.models.user
        import app.models.token
        import app.models.admin
        import app.models.waiting_list
        import app.models.resume
        import app.models.interview
        import app.models.interview_message

        # 使用同步 psycopg2 连接创建表
        sync_url = (
            f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )
        engine = create_engine(sync_url, pool_pre_ping=True)
        Base.metadata.create_all(bind=engine)
        engine.dispose()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database table creation failed: {e}")


if __name__ == "__main__":
    import uvicorn
    from app.route import create_app

    port = int(os.environ.get("PORT", settings.API_PORT))

    create_tables()

    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1,
    )
