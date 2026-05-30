# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.


import yaml
from .rules_v1 import *
from .custom_rule_engine import CustomRuleEngine

RULES = {
    "status_code": StatusCodeRule(),
    "response_time": ResponseTimeRule(),
    "headers": HeaderRule(),
    "empty_response": EmptyResponseRule(),
}

class ValidationEngine:
    def __init__(self, core_config, custom_rule_file):
        with open(core_config) as f:
            self.core_rules = yaml.safe_load(f)["rules"]

        self.custom_engine = CustomRuleEngine(custom_rule_file)

    def validate(self, response):
        # Built-in rules (fail-fast)
        for name, rule in RULES.items():
            cfg = self.core_rules.get(name)
            if cfg and cfg.get("enabled"):
                rule.validate(response, cfg)

        # Custom rules (collect results)
        results = self.custom_engine.validate(response)

        failures = [r for r in results if not r.passed]
        if failures:
            messages = "\n".join(str(f) for f in failures)
            raise AssertionError(f"Custom rule failures:\n{messages}")

        return results

