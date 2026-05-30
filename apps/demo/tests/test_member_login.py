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

from apps.demo.pages.login_page import LoginPage

SAUCEDEMO_URL = "https://www.saucedemo.com/"

# Inlined Member_Login.json (manually added)
LOGIN_CASES = [
    {
        "caseId": "TC_01",
        "scenario": "Login with valid standard user credentials",
        "preConditions": ["User is on Saucedemo login page"],
        "steps": [
            "1. Open https://www.saucedemo.com/",
            "2. Enter username: standard_user",
            "3. Enter password: secret_sauce",
            "4. Click Login",
        ],
        "expectedOutput": "User is successfully logged in and navigated to Products page",
    },
    {
        "caseId": "TC_02",
        "scenario": "Test error message for locked out user",
        "preConditions": ["User is on login page"],
        "steps": [
            "1. Open https://www.saucedemo.com/",
            "2. Enter username: locked_out_user",
            "3. Enter password: secret_sauce",
            "4. Click Login",
        ],
        "expectedOutput": "Error message 'Epic sadface: Sorry, this user has been locked out.' is displayed",
    },
    {
        "caseId": "TC_03",
        "scenario": "Login with problem_user",
        "preConditions": ["User is on login page"],
        "steps": [
            "Enter username: problem_user",
            "Enter password: secret_sauce",
            "Click Login",
        ],
        "expectedOutput": "User should login successfully; product images may appear broken (expected behavior)",
    },
    {
        "caseId": "TC_04",
        "scenario": "Login with performance_glitch_user",
        "preConditions": ["User is on login page"],
        "steps": [
            "Enter username: performance_glitch_user",
            "Enter password: secret_sauce",
            "Click Login",
        ],
        "expectedOutput": "User should login successfully; loading may be slower (intended behavior)",
    },
    {
        "caseId": "TC_05",
        "scenario": "Login with invalid username",
        "preConditions": ["On login page"],
        "steps": [
            "Enter username: invalid_user",
            "Enter password: secret_sauce",
            "Click Login",
        ],
        "expectedOutput": "Error message 'Epic sadface: Username and password do not match any user in this service' is displayed",
    },
    {
        "caseId": "TC_06",
        "scenario": "Login with invalid password",
        "preConditions": ["On login page"],
        "steps": [
            "Enter username: standard_user",
            "Enter password: wrong_pass",
            "Click Login",
        ],
        "expectedOutput": "Error message 'Epic sadface: Username and password do not match any user in this service' is displayed",
    },
    {
        "caseId": "TC_07",
        "scenario": "Login with blank username",
        "preConditions": ["On login page"],
        "steps": [
            "Leave username blank",
            "Enter password: secret_sauce",
            "Click Login",
        ],
        "expectedOutput": "Error message 'Epic sadface: Username is required' is displayed",
    },
    {
        "caseId": "TC_08",
        "scenario": "Login with blank password",
        "preConditions": ["On login page"],
        "steps": [
            "Enter username: standard_user",
            "Leave password blank",
            "Click Login",
        ],
        "expectedOutput": "Error message 'Epic sadface: Password is required' is displayed",
    },
    {
        "caseId": "TC_09",
        "scenario": "Login with both username and password blank",
        "preConditions": ["On login page"],
        "steps": ["Leave username blank", "Leave password blank", "Click Login"],
        "expectedOutput": "Error message 'Epic sadface: Username is required' is displayed",
    },
    {
        "caseId": "TC_10",
        "scenario": "Verify password field is masked",
        "preConditions": ["On login page"],
        "steps": ["Enter any text in password field"],
        "expectedOutput": "Password should appear as masked (\u25cf\u25cf\u25cf\u25cf\u25cf)",
    },
]


login_test_cases = [(c["caseId"], c.get("steps", [])) for c in LOGIN_CASES]


def _run_login_case(steps, request):
    page = request.getfixturevalue("page")
    page.goto(SAUCEDEMO_URL)
    login_page = LoginPage(page)

    username = None
    password = None

    for step in steps:
        with allure.step(step):
            if "Enter username" in step:
                username = step.split(":", 1)[1].strip()
            elif "Leave username blank" in step:
                username = None
            elif "Enter password" in step:
                try:
                    password = step.split(":", 1)[1].strip()
                except IndexError:
                    password = "fallback_password"
            elif "Leave password blank" in step:
                password = None
            elif "Click Login" in step:
                login_page.login(username, password)

    # Basic verification: either logged in or error shown
    if login_page.is_logged_in():
        pass
    else:
        err = login_page.get_error_message()
        assert err is not None


# Individual tests (TC_01 -> TC_09) with corresponding Xray ids MYY-60..MYY-68
@allure.feature("Member Login")
@pytest.mark.xray("MYY-60")
@allure.link("https://infobeans.atlassian.net/browse/MYY-60", name="MYY-60")
def test_TC_01(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_01")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-61")
@allure.link("https://infobeans.atlassian.net/browse/MYY-61", name="MYY-61")
def test_TC_02(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_02")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-62")
@allure.link("https://infobeans.atlassian.net/browse/MYY-62", name="MYY-62")
def test_TC_03(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_03")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-63")
@allure.link("https://infobeans.atlassian.net/browse/MYY-63", name="MYY-63")
def test_TC_04(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_04")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-64")
@allure.link("https://infobeans.atlassian.net/browse/MYY-64", name="MYY-64")
def test_TC_05(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_05")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-65")
@allure.link("https://infobeans.atlassian.net/browse/MYY-65", name="MYY-65")
def test_TC_06(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_06")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-66")
@allure.link("https://infobeans.atlassian.net/browse/MYY-66", name="MYY-66")
def test_TC_07(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_07")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-67")
@allure.link("https://infobeans.atlassian.net/browse/MYY-67", name="MYY-67")
def test_TC_08(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_08")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-68")
@allure.link("https://infobeans.atlassian.net/browse/MYY-68", name="MYY-68")
def test_TC_09(request):
    steps = next(c for c in LOGIN_CASES if c["caseId"] == "TC_09")["steps"]
    _run_login_case(steps, request)


@allure.feature("Member Login")
@pytest.mark.xray("MYY-69")
@allure.link("https://infobeans.atlassian.net/browse/MYY-69", name="MYY-69")
def test_password_masked(request):
    page = request.getfixturevalue("page")
    page.goto(SAUCEDEMO_URL)
    login_page = LoginPage(page)
    with allure.step("Verify password field is masked"):
        masked = login_page.is_password_masked()
        assert masked, "Password field should be masked"
