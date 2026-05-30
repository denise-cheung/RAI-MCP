# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


class StatusCodeRule:
    def validate(self, response, config):
        if response.status_code >= 500:
            raise AssertionError(f"Server error: {response.status_code}")

class ResponseTimeRule:
    def validate(self, response, config):
        if response.elapsed.total_seconds() * 1000 > config["max_ms"]:
            raise AssertionError("SLA breached")

class HeaderRule:
    def validate(self, response, config):
        for h in config["required"]:
            if h not in response.headers:
                raise AssertionError(f"Missing header: {h}")

class EmptyResponseRule:
    def validate(self, response, config):
        if not response.content:
            raise AssertionError("Empty response")
