# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


from loguru import logger
import allure
import pytest
from utils import (
    build_valid_payload,
    extract_schema,
    find_post_endpoint,
)




@allure.feature("POST APIs")
@allure.story("{endpoint_key}")
def test_post_create(
    base_url,
    headers,
    session,
    config,
    endpoint_key,
    validation_engine
):
    paths = config["_swagger_paths"]
    components = config["_swagger_components"]
    fk_cache = {}

    with allure.step("Identify POST endpoint from Swagger"):
        post_path = find_post_endpoint(endpoint_key, paths)

        if not post_path:
            logger.info("POST not supported for endpoint: %s", endpoint_key)
            pytest.skip("POST not supported")

        if post_path == "/api/token/":
            logger.info("Skipping token endpoint")
            pytest.skip("Skipping token endpoint")

        logger.info("POST endpoint resolved: %s", post_path)

    with allure.step("Extract request schema"):
        schema = extract_schema(paths[post_path]["post"])
        logger.debug("Extracted schema: %s", schema)

    with allure.step("Build valid request payload"):
        payload = build_valid_payload(
            schema=schema,
            session=session,
            paths=paths,
            fk_cache=fk_cache,
            base_url=base_url,
            components=components,
        )

        logger.info("Generated POST payload for %s: %s", endpoint_key, payload)
        allure.attach(
            str(payload),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Send POST request"):
        response = session.post(
            base_url + post_path,
            json=payload,
            headers=headers,
        )

        logger.info(
            "POST response received | status=%s | endpoint=%s",
            response.status_code,
            post_path,
        )

        allure.attach(
            response.text,
            name="POST Response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Validate POST response"):
        validation_engine.validate(response)

