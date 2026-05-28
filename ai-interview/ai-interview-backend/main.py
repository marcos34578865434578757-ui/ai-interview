import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def create_tables():
    """启动时同步创建所有数据库表"""
    try:
        from sqlalchemy import create_engine
        from app.db.models import Base
        from app.core.config import settings

        import app.models.user
        import app.models.token
        import app.models.admin
        import app.models.waiting_list
        import app.models.resume
        import app.models.interview
        import app.models.interview_message

        host = settings.POSTGRES_HOST
        port = settings.POSTGRES_PORT
        user = settings.POSTGRES_USER
        password = settings.POSTGRES_PASSWORD
        db = settings.POSTGRES_DB

        print(f"[DB] host={host} port={port} user={user} db={db}")

        sync_url = (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{host}:{port}/{db}?sslmode=require"
        )
        engine = create_engine(sync_url, pool_pre_ping=True, pool_timeout=10)
        Base.metadata.create_all(bind=engine)
        engine.dispose()
        print("[DB] Tables created OK")
    except Exception as e:
        print(f"[DB] FAILED: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8001))

    create_tables()

    from app.route import create_app

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False, workers=1)
