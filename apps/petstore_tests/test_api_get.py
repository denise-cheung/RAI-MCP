# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.



import requests
import allure
import pytest
from utils import build_valid_payload, extract_schema, find_post_endpoint, get_expected_value_from_rule

@allure.feature("GET APIs")
@allure.story("{endpoint_key}")
def test_get_collection(base_url, headers, config, endpoint_key, validation_engine):
    if endpoint_key == 'api':
        pytest.skip("GET not supported for this endpoint")
    response = requests.get(
        f"{base_url}{config[endpoint_key]['list']}",
        headers=headers
    )
    allure.attach(response.text, "Response", allure.attachment_type.JSON)
    assert response.status_code == 200
    validation_engine.validate(
        response=response,
    )


@allure.feature("GET APIs")
@allure.story("{endpoint_key}")
def test_get_by_id(base_url, headers, session, config, endpoint_key, validation_engine):
    fk_cache = {}
    paths = config["_swagger_paths"]
    components = config["_swagger_components"]

    post_path = find_post_endpoint(endpoint_key, paths)
    if (not post_path) or (post_path == '/api/token/'):
        pytest.skip("POST not supported")

    schema = extract_schema(paths[post_path]["post"])
    payload = build_valid_payload(
        schema, session, paths, fk_cache, base_url, components
    )

    create = session.post(base_url + post_path, json=payload, headers=headers)
    obj_id = create.json()["id"]
    expected_id = get_expected_value_from_rule('USER_ID_PRESENT')

    response = requests.get(
        f"{base_url}{config[endpoint_key]['detail'].format(id=obj_id)}",
        headers=headers
    )
    allure.attach(response.text, "Response", allure.attachment_type.JSON)
    assert response.status_code == 200

