import time
import uuid
from fastapi import Request
from app.utils.logging import setup_logger

logger = setup_logger("request")


async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(
        f"request_start id={request_id} "
        f"method={request.method} path={request.url.path}"
    )

    try:
        response = await call_next(request)
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"request_error id={request_id} "
            f"duration_ms={int(duration * 1000)} "
            f"error={e}"
        )
        raise

    duration = time.time() - start_time

    logger.info(
        f"request_end id={request_id} "
        f"status={response.status_code} "
        f"duration_ms={int(duration * 1000)}"
    )

    response.headers["X-Request-ID"] = request_id
    return response
