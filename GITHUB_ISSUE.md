# GitHub Issue: Auto-Run and Email Delivery Feature

Copy and paste this into a new GitHub issue:

---

## Title
Add Auto-Run Scheduling and Email Delivery

## Labels
`enhancement`, `feature-request`

## Description

### Feature Request: Automated Daily Execution with Email Delivery

**Problem:**
Currently, the healthcare news scraper must be run manually each day. Users need to remember to execute the script and then manually open the generated HTML brief.

**Proposed Solution:**
Add two new features to automate the workflow:

1. **Auto-Run Scheduling** - Automatically run the scraper at a specified time each day
2. **Email Delivery** - Email the generated brief to specified recipients

---

### Feature 1: Auto-Run Scheduling

**Requirements:**
- Schedule scraper to run automatically at a configurable time (default: 6:00 AM daily)
- Support multiple scheduling methods:
  - Windows Task Scheduler (primary)
  - WSL cron (alternative)
  - Python scheduler (fallback)
- Create wrapper script for scheduled execution
- Add logging for scheduled runs
- Handle errors gracefully

**Expected Behavior:**
- Scraper runs automatically every day at 6:00 AM (configurable)
- Generates HTML brief in `briefs/` directory
- Logs all activity to `logs/scraper_YYYY-MM-DD.log`
- Continues running even if one day fails

**Deliverables:**
- [ ] Wrapper script (`run_scraper.sh` or `.bat`)
- [ ] Configuration documentation for Task Scheduler/cron
- [ ] Logging implementation
- [ ] Setup guide in documentation

---

### Feature 2: Email Delivery

**Requirements:**
- Email generated HTML brief to specified recipients
- Support for multiple email providers:
  - Gmail (with app password or OAuth2)
  - Outlook/Office 365
  - Custom SMTP servers
- Configurable email settings (recipients, subject, etc.)
- Secure credential storage (no plain-text passwords)
- Error notification emails when scraper fails
- Support for:
  - HTML attachment delivery
  - Inline HTML email (optional)
  - Multiple recipients

**Expected Behavior:**
- After scraper completes successfully, automatically email the brief
- Recipients receive email with subject: "Healthcare News Brief - YYYY-MM-DD"
- Email includes:
  - Brief summary (article count, top categories)
  - HTML file as attachment
- If scraper fails, send error notification email with logs

**Deliverables:**
- [ ] Email sender module (`src/email_sender.py`)
- [ ] Email configuration file (`config_email.yaml`)
- [ ] Credential manager for secure password storage
- [ ] Email template (HTML)
- [ ] Integration with scraper workflow
- [ ] Documentation for email setup

---

### Combined Workflow

**End-to-End Process:**
1. Scheduled task triggers at 6:00 AM daily
2. Wrapper script runs the scraper
3. Scraper generates HTML brief
4. Email module sends brief to recipients
5. Logs all activity
6. If any step fails, send error notification email

---

### Configuration Example

**`config_email.yaml`:**
```yaml
email:
  enabled: true

  smtp:
    server: "smtp.gmail.com"
    port: 587
    use_tls: true

  sender:
    email: "your-email@gmail.com"
    name: "Healthcare News Scraper"

  recipients:
    - "recipient@example.com"

  subject: "Healthcare News Brief - {date}"

  delivery:
    method: "attachment"  # attachment, inline, or both
```

---

### Technical Details

**New Files:**
- `run_scraper.sh` or `run_scraper.bat` - Wrapper script for scheduled execution
- `src/email_sender.py` - Email delivery module
- `config_email.yaml` - Email configuration
- `src/credential_manager.py` - Secure credential storage
- `templates/email_template.html` - Email HTML template

**Dependencies:**
```
secure-smtplib (or built-in smtplib)
cryptography (for credential encryption)
```

**Integration Points:**
- Wrapper script calls `scraper_google.py`
- On success, wrapper calls `email_sender.py`
- On failure, wrapper sends error email

---

### Success Criteria

- [ ] Scraper runs automatically daily without manual intervention
- [ ] HTML brief delivered to email inbox within 5 minutes of scheduled time
- [ ] Email credentials stored securely (no plain-text passwords)
- [ ] Error notifications sent when scraper fails
- [ ] Complete documentation for setup
- [ ] Works on both Windows and WSL/Linux

---

### Priority

**High** - This feature significantly improves usability and automation

---

### Estimated Effort

**5-7 hours** total:
- Auto-run scheduling: 1-2 hours
- Email delivery: 3-4 hours
- Integration & testing: 1 hour
- Documentation: 1 hour

---

### Additional Context

See detailed design in `FEATURE_REQUEST_EMAIL_DELIVERY.md` and `SCHEDULING_GUIDE.md` for implementation details.

Current manual workflow requires:
1. Manually running script daily
2. Opening HTML file in browser
3. No email notification

Desired automated workflow:
1. Scraper runs automatically
2. Brief arrives in inbox
3. No manual action required

---

### Questions

1. Which email provider should be prioritized? (Gmail, Outlook, or both)
2. Should inline HTML email be supported or just attachments?
3. Should we support multiple recipients/distribution lists?
4. What scheduling method is preferred? (Task Scheduler vs cron vs Python)

---

