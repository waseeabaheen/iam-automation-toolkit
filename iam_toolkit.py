
### 🛠 iam_toolkit.py
```python
#!/usr/bin/env python3
"""
iam_toolkit.py

Toolkit for AWS IAM automation: user audits, stale key detection, reporting, and notifications.
"""
import argparse
import json
import csv
import os
from datetime import datetime, timezone, timedelta
import boto3
import smtplib
from email.message import EmailMessage

# ——— Config Constants ———
DEFAULT_STALE_DAYS = 90
REPORT_DIR = "reports"

# ——— Helpers ———
def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

# ——— AWS IAM Operations ———
def list_users(iam):
    paginator = iam.get_paginator('list_users')
    users = []
    for page in paginator.paginate():
        for u in page['Users']:
            users.append({
                'UserName': u['UserName'],
                'CreateDate': u['CreateDate'].strftime('%Y-%m-%d'),
                'PasswordLastUsed': u.get('PasswordLastUsed', '').strftime('%Y-%m-%d') if u.get('PasswordLastUsed') else ''
            })
    return users


def list_access_keys(iam):
    users = iam.list_users()['Users']
    keys = []
    for u in users:
        for k in iam.list_access_keys(UserName=u['UserName'])['AccessKeyMetadata']:
            keys.append({
                'UserName': u['UserName'],
                'AccessKeyId': k['AccessKeyId'],
                'Status': k['Status'],
                'CreateDate': k['CreateDate']
            })
    return keys

# ——— Reporting ———
def save_report(data, fmt, filename):
    ensure_dir(REPORT_DIR)
    path = os.path.join(REPORT_DIR, filename)
    if fmt == 'csv':
        fieldnames = data[0].keys() if data else []
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    print(f"[+] Report generated: {path}")

# ——— Notifications ———
def send_email(smtp_config, subject, body, attachments=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = smtp_config['from_addr']
    msg['To'] = ', '.join(smtp_config['to_addrs'])
    msg.set_content(body)

    if attachments:
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=os.path.basename(file_path))

    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.send_message(msg)
    print(f"[+] Email sent to {smtp_config['to_addrs']}")

# ——— Main CLI ———
def main():
    parser = argparse.ArgumentParser(description='AWS IAM Automation Toolkit')
    parser.add_argument('--report', choices=['users', 'keys'], required=True, help='Type of report to generate')
    parser.add_argument('--format', choices=['csv', 'json'], default='json', help='Report format')
    parser.add_argument('--stale-days', type=int, default=DEFAULT_STALE_DAYS, help='Days threshold for stale keys')
    parser.add_argument('--notify', action='store_true', help='Send email reminders')
    parser.add_argument('--smtp-config', help='Path to SMTP config JSON')
    args = parser.parse_args()

    iam = boto3.client('iam')
    if args.report == 'users':
        data = list_users(iam)
        filename = f"users_report_{datetime.now().strftime('%Y%m%d')}.{args.format}"
        save_report(data, args.format, filename)

    else:
        keys = list_access_keys(iam)
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.stale_days)
        stale = [
            {'UserName': k['UserName'], 'AccessKeyId': k['AccessKeyId'], 'Status': k['Status'], 'CreateDate': k['CreateDate'].strftime('%Y-%m-%d')}
            for k in keys if k['CreateDate'] < cutoff
        ]
        filename = f"stale_keys_{datetime.now().strftime('%Y%m%d')}.{args.format}"
        save_report(stale, args.format, filename)

        if args.notify and args.smtp_config:
            smtp = json.load(open(args.smtp_config))
            send_email(smtp, "Stale IAM Keys Report", "Please rotate your stale keys.", [os.path.join(REPORT_DIR, filename)])

if __name__ == '__main__':
    main()
