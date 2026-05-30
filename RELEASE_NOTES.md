<!--
Copyright (c) 2026 InfoBeans
Internal Authors: InfoBeans Accelerator Team
All rights reserved.

This software is proprietary and confidential.
Unauthorized copying, distribution, modification, or use
of this software, via any medium, is strictly prohibited.

This package is intended for internal enterprise use only.
-->

# Release Notes

## Version 0.1.0-beta.3 — 2026-02-26

> **Beta Release**
>
> This is a beta version of the `infobeans-rai` package released for early access,
> evaluation, and feedback. APIs, configuration schemas, and execution workflows
> may change without backward compatibility. This version is **not recommended
> for production use**.

---

### Overview

This release marks the initial beta availability of the `infobeans-rai` QA automation
framework. The primary objective of this beta is to validate the core framework
architecture, CI/CD integration, and test management workflows in real-world
enterprise environments.

---

### New Features

- Initial beta release of the `infobeans-rai` QA automation framework
- Support for **pytest** as the primary test execution engine
- HTML-based test report generation for execution results
- Integration with **Jira Xray** for test case management and result publishing
- One-click test execution through preconfigured **GitHub Actions** workflows
- Scaffolding support for creating and organizing:
  - Test  configurations
  - Project structure
  - GitHub Actions workflow templates

---

### Known Limitations

- Configuration schema validation is minimal and may allow invalid configurations
- Reporting is currently limited to HTML format
- Advanced capabilities such as:
  - Configurable parallel execution
  - Allure reporting
  are not available in this release
- Error handling, logging, and diagnostic messages are basic and will be expanded
  in subsequent beta releases

---

### Breaking Changes

- Not applicable (initial beta release)

---

### Security

- No known security vulnerabilities have been identified in this release
- The package has not yet undergone a formal security or penetration review
- Secrets and credentials are expected to be managed via CI/CD environment
  variables or secure secret stores (e.g., GitHub Secrets)

---

### Feedback Requested

Feedback is especially requested on the following areas:
- Usability and clarity of test  scaffolding and configuration structure
- Stability and reliability of execution via GitHub Actions
- Completeness, reliability, and ease of use of the Jira Xray integration

---

### Next Steps

Planned enhancements for upcoming beta releases include:
- Stronger configuration schema validation and improved error handling
- Enhanced reporting capabilities, including Allure report integration
- Support for configurable and scalable parallel test execution

---