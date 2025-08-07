# IAM Automation Toolkit

Automate AWS IAM user auditing, access key rotation warnings, and generate certification-ready reports.

## About
A Python-based toolkit for automating AWS IAM tasks: user auditing, stale key detection, and certification-ready reporting. Designed to streamline access reviews and credential hygiene for security teams.

## Features
- **List IAM Users** with creation dates, last password use, and attached policies
- **Detect Stale Access Keys** older than a configurable number of days
- **Generate Reports** in JSON or CSV formats for easy integration
- **Email Notifications** for key rotation reminders via SMTP configuration

## Requirements
- Python 3.7+
- AWS credentials configured (via `~/.aws/credentials` or environment variables)
- Python packages: `boto3`

## Installation
```bash
# Clone the repository
git clone https://github.com/your-username/iam-automation-toolkit.git
cd iam-automation-toolkit

# (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

## Usage
# 1. Generate a user audit report (CSV)
python iam_toolkit.py --report users --format csv
ATH
# 2. Detect keys older than 60 days and output JSON
python iam_toolkit.py --report keys --stale-days 60 --format json

# 3. Run stale key detection and send email reminders
python iam_toolkit.py --report keys --notify --smtp-config $SMTP_CONFIG_P

## Configuration

Adjust the constants at the top of `iam_toolkit.py`:
```python
# Days before a key is considered stale
default_stale_days = 90

# Directory to save JSON/CSV reports
REPORT_DIR = "reports"

# SMTP config JSON file path for email notifications
SMTP_CONFIG_PATH = "smtp_config.json"
