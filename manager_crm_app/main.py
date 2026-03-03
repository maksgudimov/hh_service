import os
from dotenv import load_dotenv
from uvicorn import run

from service.app_configuration import create_service


env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(override=True, dotenv_path=env_path)


app = create_service()


if __name__ == "__main__":
    run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        log_level="info",
        forwarded_allow_ips="*",
        headers=[("X-API-Version", "v1")],
    )
