import os
from dataclasses import dataclass
from pathlib import Path
from os import environ as environment


BASE_DIR = Path(__file__).parent.parent.parent


@dataclass(frozen=True)
class AuthJWTConfig:
    private_key_path: Path = Path(BASE_DIR) / 'certs' / 'jwt-private.pem'
    public_key_path: Path = Path(BASE_DIR) / 'certs' / 'jwt-public.pem'
    algorithm: str = environment["ALGORITHM"]
    access_token_expire_minutes: int = 15
