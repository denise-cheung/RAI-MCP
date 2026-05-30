# Copyright (c) 2026 InfoBeans
# Internal Authors: InfoBeans Accelerator Team
# All rights reserved.
#
# This software is proprietary and confidential.
# Unauthorized copying, distribution, modification, or use
# of this software, via any medium, is strictly prohibited.
#
# This package is intended for internal enterprise use only.



class RuleResult:
    def __init__(self, rule_id, passed, reason=None, actual_value=None, expected_value=None):
        self.rule_id = rule_id
        self.passed = passed
        self.reason = reason
        self.actual_value = actual_value
        self.expected_value = expected_value

    def __repr__(self):
        if self.reason and self.reason.startswith("SKIPPED"):
            return f"[SKIPPED] {self.rule_id}"
        status = "PASS" if self.passed else "FAIL"
        msg = f"[{status}] {self.rule_id}: {self.reason or ''}"
        if not self.passed and self.actual_value is not None:
            msg += f" (actual: {self.actual_value}"
            if self.expected_value is not None:
                msg += f", expected: {self.expected_value}"
            msg += ")"
        return msg

