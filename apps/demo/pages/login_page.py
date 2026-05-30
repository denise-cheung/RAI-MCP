# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = 'input[data-test="username"]'
        self.password_input = 'input[data-test="password"]'
        self.login_button = 'input[data-test="login-button"]'
        self.error_message = 'h3[data-test="error"]'

    def login(self, username=None, password=None):
        if username is not None:
            self.page.fill(self.username_input, username)
        else:
            self.page.fill(self.username_input, "")
        if password is not None:
            self.page.fill(self.password_input, password)
        else:
            self.page.fill(self.password_input, "")
        self.page.click(self.login_button)

    def is_logged_in(self):
        return self.page.is_visible(".inventory_list")

    def get_error_message(self):
        if self.page.is_visible(self.error_message):
            return self.page.inner_text(self.error_message)
        return None

    def is_password_masked(self):
        input_type = self.page.get_attribute(self.password_input, "type")
        return input_type == "password"
