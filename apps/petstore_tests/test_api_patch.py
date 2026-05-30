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

@allure.feature("PATCH APIs")
@allure.story("Partially update existing resource")
def test_patch_update(
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
            pytest.skip("Auth endpoint should not be tested for PATCH")

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
    # STEP 4: Perform PATCH update (partial)
    # -------------------------------------------------
    with allure.step(f"Partially update resource via PATCH (id={expected_id})"):
        patch_url = base_url + config[endpoint_key]["detail"].format(id=expected_id)
        
        # Use only a subset of fields for partial update
        patch_payload = {k: v for i, (k, v) in enumerate(payload.items()) if i < 2}

        patch_resp = session.patch(
            patch_url,
            json=patch_payload,
            headers=headers
        )

    # -------------------------------------------------
    # STEP 5: Validate response using rule engine
    # -------------------------------------------------
    with allure.step("Validate PATCH response using validation engine"):
        validation_engine.validate(patch_resp)

