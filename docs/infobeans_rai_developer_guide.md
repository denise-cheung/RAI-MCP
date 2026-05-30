<!--
Copyright (c) 2026 InfoBeans
Internal Authors: InfoBeans Accelerator Team
All rights reserved.

This software is proprietary and confidential.
Unauthorized copying, distribution, modification, or use
of this software, via any medium, is strictly prohibited.

This package is intended for internal enterprise use only.
-->

## Technical Architecture Overview

infobeans-rai is a comprehensive test automation framework built on Python 3.12+ with Playwright, Pytest. The framework implements a modular architecture supporting JIRA-Xray Integration, Parallel Processing, HTML Reporting, Email, Teams and  Slack Notifications.

## 🚀 Quick Start Setup

For comprehensive setup instructions including all dependencies, credentials, and integrations, refer to [`infobeans_rai_setup_guide.md`](infobeans_rai_setup_guide.md).

### **Essential Setup Checklist**

#### **1. Environment Setup**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install infobeans_rai-0.1.0b3-py3-none-any.whl

# Install Playwright browsers
playwright install

# Creates basic sample test  to run locally/github actions workflow along with configuration files.
infobeans-rai setup --app appname --scaffold true

# Creates full template with all test s (UI, API, DB tests, helpers, utils, test data).
infobeans-rai setup --app appname --scaffold full

# Creates bare minimum configuration and a test file along with github actions workflow files.
infobeans-rai setup --app appname --scaffold false

# Sets up pipeline-related files (.github, requirements.txt, docs, etc.) in the root directory.
infobeans-rai setup-pipeline

infobeans-rai run \
  --app saucedemoapp \        # Application name (must match folder under apps/)
  --config config.yaml \      # Environment-specific configuration file
  --workers-count 4 \         # Number of parallel test workers
  --split-level module \      # Split levels (test_file/module)
  --reruns 2 \                # Retry failed tests
  --reruns-delay 2            # Delay (in seconds) between retries
  --debug-level INFO          # INFO, DEBUG, WARNING, ERROR, CRITICAL


```

#### **2. Required Credentials**
Ensure the following environment variables or secrets are configured:

| Service | Required Credentials | Setup Guide |
|---------|---------------------|-------------|

| **Jira Xray** | `XRAY_CLIENT_ID`, `XRAY_CLIENT_SECRET`, `XRAY_API_BASE_URL`, `XRAY_PROJECT_KEY` | [Setup Guide](https://docs.getxray.app/display/XRAY/Installation) |
| **Slack** | `SLACK_WEBHOOK_URL`, `SLACK_TOKEN` | [Setup Guide](https://api.slack.com/messaging/webhooks) |
| **MS Teams** | `WEBHOOK_URL` | [Setup Guide](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) |
| **Gmail** | `GMAIL_USERNAME`, `GMAIL_APP_PASSWORD` | [Setup Guide](https://support.google.com/accounts/answer/185833) |

## Core Technology Stack

### **Primary Technologies**
- **Python 3.12+**: Core programming language
- **Playwright**: Modern browser automation (replaces Selenium)
- **Pytest**: Test framework with extensive plugin ecosystem

### **Supporting Libraries**
- **pytest-xdist**: Parallel test execution
- **pytest-html**: HTML report generation
- **pytest-jira-xray**: Jira Xray integration for test management
- **pytest-playwright**: Playwright-Pytest integration
- **requests**: HTTP client for API testing
- **reportlab**: PDF report generation

## Configuration Management

### **Environment-Based Configuration**
```yaml
# config.yaml
# Automation Suite Specific Configs as your .

# Framework Specific Configs
reporting:
  # Enable and configure reporting plugins.
  - name: HtmlReportPlugin
    enabled: true
  - name: XrayPlugin
    enabled: true
    config: {
      XRAY_CLIENT_ID: "${XRAY_CLIENT_ID}",
      XRAY_CLIENT_SECRET: "${XRAY_CLIENT_SECRET}",
      XRAY_API_BASE_URL: "${XRAY_API_BASE_URL}",
      XRAY_PROJECT_KEY: "${XRAY_PROJECT_KEY}",
    }

```
## CI/CD Pipeline Deep Dive

### **GitHub Actions Pipeline Features**

#### **Execution Modes**
```yaml
workflow_dispatch:
  inputs:
    mode:
      description: "Execution mode"
      type: choice
      options:
        - parallel-with-pytest      # pytest-xdist parallel execution
```

#### **Parallel Execution Strategies**
```bash
# Parallel with infobeans-rai
  infobeans-rai run --app demoapp --config config.yaml --workers-count auto --split-level module --reruns 2 --reruns-delay 10 --debug-level INFO

  --app       		# Application name (must match folder under apps/)
  --config    		# Environment-specific configuration file
  --workers-count 	# Number of parallel test workers
  --split-level module  # Split levels (test_file/module)
  --reruns 2		# Retry failed tests
  --reruns-delay 2	# Delay (in seconds) between retries
  --debug-level INFO        # INFO, DEBUG, WARNING, ERROR, CRITICAL
```

#### **Artifact Management**
```yaml
- name: Upload test reports
  uses: actions/upload-artifact@v4
  with:
    name: pytest-reports
    path: |
      reports/**
      test-results.xml
      test-results.json
```

## Reporting and Evidence Collection

### **PDF Reporting**
```python
# framework/core/utilsgenerate_pytest_report.py
def generate_report():
    """
    Generates multiple report formats:
    - PDF: Executive summary reports
    """
```

## Notification and Alerting

### **Multi-Channel Notifications**
```yaml
# Slack Integration
- name: Slack Notification
  uses: rtCamp/action-slack-notify@v2
  env:
    SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK_URL }}
    SLACK_CHANNEL: general

# Microsoft Teams Integration
- name: MS Teams Message Card
  uses: simbo/msteams-message-card-action@v1.4.3
  with:
    webhook: ${{ secrets.WEBHOOK_URL }}

# Email Notifications
- name: Send email notification
  uses: dawidd6/action-send-mail@v6
  with:
    server_address: smtp.gmail.com
    attachments: "report.zip,test_summary.pdf"
```

## Troubleshooting and Debugging

### **Debug Mode Configuration**
```bash
# Verbose logging for debugging
  infobeans-rai run --app demoapp --config config.yaml --workers-count auto --split-level module --reruns 2 --reruns-delay 10 --debug-level INFO

  --app       		# Application name (must match folder under apps/)
  --config    		# Environment-specific configuration file
  --workers-count 	# Number of parallel test workers
  --split-level module  # Split levels (test_file/module)
  --reruns 2		# Retry failed tests
  --reruns-delay 2	# Delay (in seconds) between retries
  --debug-level INFO        # INFO, DEBUG, WARNING, ERROR, CRITICAL
```

### **Failure Analysis Tools**
```python
# Automatic screenshot capture on failure
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # Capture DOM snapshot and screenshot
        capture_debug_info(item, call.excinfo)
```

## General Development Guidelines

### **Development**
- Follow the method documenting style as follows
```python
def method_name(self, param1, param2):
    """
    Description of the method
    :param param1: Description of param1    
    :param param2: Description of param2
    :return: Description of return value
    :raises Exception: Description of exception
    """
    # Method implementation
```

- Follow the variable naming convention as follows
```python
variable_name = value
```

- Follow the class naming convention as follows
```python
class ClassName:
    """
    Description of the class
    """
    # Class implementation
```

- Follow the class method naming convention as follows
```python
def method_name(self, param1, param2):
    """
    Description of the method
    :param param1: Description of param1    
    :param param2: Description of param2
    :return: Description of return value
    :raises Exception: Description of exception
    """
    # Method implementation
```

- Follow the class attribute naming convention as follows
```python
attribute_name = value
```

- Follow the class attribute documenting style as follows
```python
attribute_name = value
    """
    Description of the attribute
    """
```
- make sure to run sca in local dev environment to validate the code quality.
- make sure to run pytest in local dev environment to validate the test coverage.

---

This comprehensive framework provides a solid foundation for scalable, maintainable test automation that adapt to application changes while maintaining high reliability and performance standards.
