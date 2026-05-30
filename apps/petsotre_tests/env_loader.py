# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


# swagger_test_generator/env_loader.py
import os
from pathlib import Path
import yaml


class EnvConfig:
    def __init__(self, env_name: str):
        self.env_name = env_name
        self.config_path = self._resolve_config_path()
        self.envs = self._load_envs()

        if env_name not in self.envs:
            raise ValueError(
                f"Unknown environment '{env_name}'. "
                f"Available: {list(self.envs.keys())}"
            )

        self.env = self.envs[env_name]

    def _resolve_config_path(self) -> Path:
        
        env_path = os.getenv("ENV_CONFIG_FILE")
        if env_path:
            path = Path(env_path).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(
                    f"ENV_CONFIG_FILE set but file not found: {path}"
                )
            return path

        fallback = Path.cwd() / "environments.yaml"
        if fallback.exists():
            return fallback

        raise FileNotFoundError(
            "environments.yaml not found. Set ENV_CONFIG_FILE=/path/to/environments.yaml"
        )

    def _load_envs(self):
        with self.config_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def base_url(self):
        return os.getenv("BASE_URL", self.env["base_url"])

    def auth_headers(self):
        auth = self.env.get("auth")
        if not auth:
            return {}

        if auth["type"] == "jwt":
            import requests
            username = os.getenv(auth["username_env"])
            password = os.getenv(auth["password_env"])

            if not username or not password:
                raise RuntimeError("JWT credentials missing")

            resp = requests.post(
                self.base_url() + auth["token_url"],
                json={"username": username, "password": password},
                timeout=10,
            )
            resp.raise_for_status()

            return {"Authorization": f"Bearer {resp.json()['access']}"}

        raise ValueError(f"Unsupported auth type: {auth['type']}")

