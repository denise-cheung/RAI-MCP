# RAI MCP — InfoBeans AI Test Automation Workspace

AI-powered QA test automation using the InfoBeans RAI MCP server. Generates, runs, and reports on API test suites from OpenAPI/Swagger specs — with CI/CD, Allure reporting, and Jira Xray integration built in.

---

## What This Workspace Does

- **Generates API tests** from any Swagger/OpenAPI schema URL — no manual test writing
- **Runs tests** in parallel with retry logic and Allure reporting
- **Produces executive PDF reports** from test results
- **Integrates with Jira Xray** for test management
- **Ships with GitHub Actions pipelines** for CI/CD out of the box

---

## Project Structure

```
RAI-MCP/
├── apps/                        # Test suites (one folder per app)
│   ├── demo/                    # Sample Playwright login test
│   └── petstore_tests/          # Petstore API tests (generated from Swagger)
├── .github/
│   ├── workflows/
│   │   ├── MasterPipeline.yml   # Main test execution pipeline
│   │   └── StaticCodeAnalysis.yml
│   └── templates/
│       └── email-template.html
├── docs/                        # Framework documentation
├── vendor/                      # Offline install package
├── requirements.txt
├── environments.yaml            # Environment config (base URLs, etc.)
└── .env_sample                  # Credential template — copy to .env and fill in
```

---

## Quickstart

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env_sample .env
# Edit .env with your Xray, Jira, and notification credentials
```

### 3. Generate tests from a Swagger schema

Use the InfoBeans RAI MCP in Claude Desktop or Claude Code CLI:

```
Generate API tests from https://your-api/swagger.json into a folder called my_app_tests
```

### 4. Run tests

```
Run the my_app_tests test suite using the infobeans-rai MCP
```

### 5. Generate a report

```
Generate a PDF report for the my_app_tests run
```

---

## GitHub Actions Setup

The pipelines in `.github/workflows/` are ready to use. Add these secrets to your repo under **Settings → Secrets and variables → Actions**:

| Secret | Purpose |
|--------|---------|
| `SLACK_WEBHOOK_URL`, `SLACK_TOKEN` | Slack notifications |
| `WEBHOOK_URL` | MS Teams notifications |
| `GMAIL_USERNAME`, `GMAIL_APP_PASSWORD`, `NOTIFICATION_EMAIL` | Email notifications |
| `XRAY_CLIENT_ID`, `XRAY_CLIENT_SECRET`, `XRAY_PROJECT_KEY` | Jira Xray integration |
| `GITHUB_TOKEN` | Allure report deployment (auto-provided by GitHub) |

---

## MCP Setup (Claude Code CLI)

The `.mcp.json` in this repo pre-configures the `infobeans-rai` MCP server. Launch Claude Code CLI from this directory and the server connects automatically:

```bash
cd /path/to/RAI-MCP
claude
```

---

## Documentation

See the `docs/` folder for:
- Setup guide
- Developer guide
- Pipeline features reference
- Folder structure reference
