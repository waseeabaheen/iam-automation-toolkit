# iam-automation-toolkit
# IAM Automation Toolkit

Automate AWS IAM user auditing, access key rotation warnings, and generate certification-ready reports.

## Features

- **List IAM Users** with creation dates and attached policies
- **Detect Stale Access Keys** older than configurable days
- **Generate PDF/CSV Reports** (users, keys, policies)
- **Send Email Notifications** for key rotation reminders

## Requirements

- Python 3.7+
- AWS credentials configured (via `~/.aws/credentials` or environment variables)

## Installation

```bash
git clone https://github.com/your-username/iam-automation-toolkit.git
cd iam-automation-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
