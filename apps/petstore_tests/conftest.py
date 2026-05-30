# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pytest
import requests
from config import config as _config
from validation.rule_engine import ValidationEngine
from env_loader import EnvConfig
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("TEST_ENV", "dev")
AUTH_NEEDED = os.getenv("AUTH_NEEDED", "false").lower() == "true"

@pytest.fixture(scope="session")
def env():
    return EnvConfig(ENV)

@pytest.fixture(scope="session")
def base_url(env):
    return env.base_url()

@pytest.fixture(scope="session")
def session():
    return requests.Session()

@pytest.fixture(scope="session")
def headers(env):
    headers = {"Content-Type": "application/json"}
    if AUTH_NEEDED:
        headers.update(env.auth_headers())
    return headers

@pytest.fixture(scope="session")
def config():
    return _config

@pytest.fixture(scope="session")
def validation_engine():
    base_dir = Path(__file__).resolve().parent
    return ValidationEngine(
        base_dir / "validation" / "config.yaml",
        base_dir / "validation" / "custom_rules.yaml"
    )

def pytest_generate_tests(metafunc):
    if "endpoint_key" in metafunc.fixturenames:
        endpoints = [k for k in _config if not k.startswith("_")]
        metafunc.parametrize("endpoint_key", endpoints)
