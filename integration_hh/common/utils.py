from fastapi import Request, HTTPException
import os
from os import environ as environment
from pathlib import Path

from dotenv import load_dotenv


env_path = os.path.join(Path(__file__).parent.parent.parent.parent, ".env")
load_dotenv(override=True, dotenv_path=env_path)


def check_token_hh(request: Request):
    header_auth = request.headers.get("Authorization")
    token = header_auth.split("Bearer ")[1]
    if token != environment["X_API_KEY_HH"]:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return
