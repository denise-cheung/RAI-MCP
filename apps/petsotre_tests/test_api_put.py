# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


import allure
import pytest
from utils import (
    find_post_endpoint,
    build_valid_payload,
    extract_schema,
    get_expected_value_from_rule
)

@allure.feature("PUT APIs")
@allure.story("Update existing resource")
def test_put_update(
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

    # -------------------------------------------------
    # STEP 1: Identify POST endpoint (for create)
    # -------------------------------------------------
    with allure.step("Identify POST endpoint for resource creation"):
        post_path = find_post_endpoint(endpoint_key, paths)

        if not post_path:
            pytest.skip("POST not supported for this resource")

        if post_path == "/api/token/":
            pytest.skip("Auth endpoint should not be tested for PUT")

    # -------------------------------------------------
    # STEP 2: Build valid payload using schema
    # -------------------------------------------------
    with allure.step("Build valid payload with all required fields"):
        post_schema = extract_schema(paths[post_path]["post"])

        payload = build_valid_payload(
            schema=post_schema,
            session=session,
            paths=paths,
            fk_cache=fk_cache,
            base_url=base_url,
            components=components
        )

        assert payload, "Generated payload is empty"

    # -------------------------------------------------
    # STEP 3: Create resource (POST)
    # -------------------------------------------------
    with allure.step("Create resource via POST"):
        create_resp = session.post(
            base_url + post_path,
            json=payload,
            headers=headers
        )

        assert create_resp.status_code in (200, 201), (
            f"Create failed: {create_resp.text}"
        )

        obj_id = create_resp.json().get("id")
        expected_id = get_expected_value_from_rule('USER_ID_PRESENT')
        assert obj_id, "ID not returned in POST response"

    # -------------------------------------------------
    # STEP 4: Perform PUT update
    # -------------------------------------------------
    with allure.step(f"Update resource via PUT (id={expected_id})"):
        put_url = base_url + config[endpoint_key]["detail"].format(id=expected_id)

        put_resp = session.put(
            put_url,
            json=payload,
            headers=headers
        )

    # -------------------------------------------------
    # STEP 5: Validate response using rule engine
    # -------------------------------------------------
    with allure.step("Validate PUT response using validation engine"):
        validation_engine.validate(put_resp)

