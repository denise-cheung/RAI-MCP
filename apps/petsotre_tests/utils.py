# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


import re
import os
import yaml

FK_REGEX = re.compile(r"Foreign key reference - (\w+)")

def extract_schema(operation):
    return (
        operation.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )

def resolve_schema(schema, components):
    if not schema:
        return {}
    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        return resolve_schema(components["schemas"][ref], components)
    return schema

def default_value(prop, field_name=""):
    if not prop:
        return "test"
    if prop.get("type") == "integer":
        return 1
    if prop.get("type") == "boolean":
        return True
    if prop.get("format") == "email" or "email" in field_name.lower():
        return "test@example.com"
    return "test"

def detect_foreign_keys(schema):
    fks = {}
    for field, prop in schema.get("properties", {}).items():
        desc = prop.get("description", "")
        m = FK_REGEX.search(desc)
        if m:
            fks[field] = m.group(1)
    return fks

def find_post_endpoint(resource, paths):
    for path, ops in paths.items():
        if resource.lower() in path.lower() and "post" in ops:
            return path
    return None

def build_valid_payload(schema, session, paths, fk_cache, base_url, components):
    payload = {}
    schema = resolve_schema(schema, components)
    if not schema:
        return payload

    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for field, resource in detect_foreign_keys(schema).items():
        payload[field] = create_fk(
            session, resource, paths, fk_cache, base_url, components
        )

    for field in required:
        payload.setdefault(field, default_value(properties.get(field), field))

    return payload

def create_fk(session, resource, paths, fk_cache, base_url, components):
    if resource in fk_cache:
        return fk_cache[resource]

    post_path = find_post_endpoint(resource, paths)
    schema = extract_schema(paths[post_path]["post"])
    schema = resolve_schema(schema, components)

    payload = build_valid_payload(
        schema, session, paths, fk_cache, base_url, components
    )

    resp = session.post(base_url + post_path, json=payload)
    resp.raise_for_status()

    fk_cache[resource] = resp.json()["id"]
    return fk_cache[resource]

def get_expected_value_from_rule(rule_id):
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(TEST_DIR, "validation", "custom_rules.yaml")

    with open(config_file, "r") as file:
        data = yaml.safe_load(file)

    for rule in data.get("custom_rules", []):
        if rule.get("id") == rule_id:
            return rule.get("expected")

    return None
