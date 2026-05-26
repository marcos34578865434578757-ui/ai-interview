import os
from app.route import create_app
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", settings.API_PORT))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        workers=1,
    )
