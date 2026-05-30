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
import yaml
from jsonpath_ng import parse
from .rule_result import RuleResult


class CustomRuleEngine:
    def __init__(self, rule_file):
        with open(rule_file) as f:
            self.rules = yaml.safe_load(f)["custom_rules"]

    def _extract_all(self, body, jsonpath):
        if body is None or not jsonpath:
            return []

        try:
            expr = parse(jsonpath)
            matches = expr.find(body)
            return [match.value for match in matches]
        except Exception:
            # Invalid JSONPath or evaluation error
            return []

    def _normalize_value(self, value):
        
        if isinstance(value, list):
            return value[0] if value else None
        return value

    def validate(self, response):
        results = []
        body = response.json()

        for rule in self.rules:
            rule_id = rule["id"]
            rule_type = rule["type"]
            jsonpath = rule.get("jsonpath")

            try:
                values = self._extract_all(body, jsonpath)

                # RULE APPLICABILITY CHECK
                if not values:
                    results.append(
                        RuleResult(rule_id, True, "SKIPPED: field not present")
                    )
                    continue

                passed = True
                failed_actual = None
                failed_expected = None

                for actual in values:
                    actual = self._normalize_value(actual)

                    # If value cannot be normalized, fail rule
                    if actual is None:
                        passed = False
                        failed_actual = actual
                        break

                    if rule_type == "equality":
                        expected = rule["expected"]
                        result = (actual == expected)
                        if rule.get("negate"):
                            result = not result
                        if not result:
                            failed_actual = actual
                            failed_expected = expected

                    elif rule_type == "regex":
                        result = bool(re.match(rule["pattern"], str(actual)))
                        if not result:
                            failed_actual = actual
                            failed_expected = rule["pattern"]

                    elif rule_type == "range":
                        if not isinstance(actual, (int, float)):
                            result = False
                            failed_actual = actual
                            failed_expected = f"[{rule['min']}, {rule['max']}]"
                        else:
                            result = rule["min"] <= actual <= rule["max"]
                            if not result:
                                failed_actual = actual
                                failed_expected = f"[{rule['min']}, {rule['max']}]"

                    elif rule_type == "conditional":
                        condition = rule.get("if")
                        then = rule.get("then")

                        # Invalid rule definition  PASS
                        if not condition or not then:
                            result = True

                        else:
                            if_values = self._extract_all(
                                body, condition.get("jsonpath")
                            )
                            if_values = [
                                self._normalize_value(v) for v in if_values
                            ]

                            # IF field missing  SKIP
                            if not if_values:
                                result = True

                            # IF condition matched
                            elif condition.get("equals") in if_values:
                                then_values = self._extract_all(
                                    body, then.get("jsonpath")
                                )
                                then_values = [
                                    self._normalize_value(v) for v in then_values
                                ]

                                # THEN field missing  FAIL
                                if not then_values:
                                    result = False
                                else:
                                    result = then.get("equals") in then_values

                            # IF condition not met  PASS
                            else:
                                result = True
                    else:
                        raise ValueError(f"Unknown rule type: {rule_type}")

                    if not result:
                        passed = False
                        break

                results.append(
                    RuleResult(
                        rule_id,
                        passed,
                        None if passed else rule["message"],
                        actual_value=failed_actual if not passed else None,
                        expected_value=failed_expected if not passed else None
                    )
                )

            except Exception as e:
                results.append(
                    RuleResult(rule_id, False, f"Execution error: {e}")
                )

        return results




