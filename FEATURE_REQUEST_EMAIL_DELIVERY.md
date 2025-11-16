# Feature Request: Auto-Run with Email Delivery

**Status:** 📋 Planned
**Priority:** High
**Estimated Effort:** 2-3 hours

---

## Overview

Build an automated daily scheduling system that:
1. Runs the healthcare news scraper at a specified time each day
2. Generates the categorized HTML brief
3. Emails the brief to specified recipients
4. Logs all activity for monitoring

---

## Requirements

### 1. Automated Scheduling ✅ (Documented)
- Run scraper daily at configurable time (default: 6:00 AM)
- Support multiple scheduling methods:
  - Windows Task Scheduler (primary)
  - WSL cron (alternative)
  - Python scheduler (fallback)

### 2. Email Delivery 🔨 (To Build)
- **Recipients:** Configurable email list
- **Subject:** "Healthcare News Brief - [Date]"
- **Body:** Option to send HTML inline OR as attachment
- **Attachment:** HTML file (healthcare_brief_google_YYYY-MM-DD.html)
- **Sender:** Configurable email account
- **Format:** Professional email template

### 3. Email Configuration 🔨 (To Build)
- Support multiple email providers:
  - Gmail (OAuth2 or app password)
  - Outlook/Office 365
  - Custom SMTP server
- Secure credential storage (not in plain text)
- Email template customization

### 4. Error Handling & Notifications 🔨 (To Build)
- Send failure notification email if scraper fails
- Include error details and logs
- Retry mechanism (optional)
- Daily summary email with stats

### 5. Logging & Monitoring 🔨 (To Build)
- Log all email sends (success/failure)
- Track email delivery status
- Monitor bounce-backs
- Generate weekly summary report

---

## Technical Design

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Scheduling Layer                          │
│  (Windows Task Scheduler / Cron / Python Scheduler)         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Wrapper Script                              │
│  - Runs scraper                                              │
│  - Checks for errors                                         │
│  - Calls email sender                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Scraper        │     │  Email Sender    │
│  (Existing)     │     │  (New Module)    │
│                 │     │                  │
│  - Fetch news   │     │  - Format email  │
│  - Deduplicate  │     │  - Send via SMTP │
│  - Categorize   │     │  - Log results   │
│  - Generate HTML│     │  - Handle errors │
└─────────────────┘     └─────────────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Logs & Reports                            │
│  - Scraper logs                                              │
│  - Email delivery logs                                       │
│  - Error logs                                                │
└─────────────────────────────────────────────────────────────┘
```

### New Files to Create

1. **`src/email_sender.py`** - Core email module
   - SMTP configuration
   - Email formatting
   - Attachment handling
   - Error handling

2. **`config_email.yaml`** - Email configuration
   - SMTP settings
   - Recipient list
   - Email template
   - Credentials (encrypted)

3. **`src/credential_manager.py`** - Secure credential storage
   - Encrypt/decrypt email passwords
   - OAuth2 token management
   - Keychain integration (optional)

4. **`run_scraper_and_email.sh`** - Wrapper script
   - Run scraper
   - Check results
   - Send email
   - Log everything

5. **`templates/email_template.html`** - Email HTML template
   - Professional design
   - Brief summary
   - Link to full report (if attached)

---

## Implementation Plan

### Phase 1: Email Core (Essential)

**Tasks:**
- [ ] Create `email_sender.py` module
- [ ] Create `config_email.yaml` configuration
- [ ] Implement basic SMTP email sending
- [ ] Test with Gmail using app password
- [ ] Add attachment support (HTML file)
- [ ] Create simple email template

**Deliverables:**
- Working email sender that can send HTML briefs as attachments
- Configuration file for email settings

**Testing:**
- Send test email to yourself
- Verify attachment is readable
- Confirm formatting is correct

### Phase 2: Integration (Essential)

**Tasks:**
- [ ] Create `run_scraper_and_email.sh` wrapper
- [ ] Integrate scraper with email sender
- [ ] Add error handling (email on failure)
- [ ] Create logging for email sends
- [ ] Test end-to-end workflow

**Deliverables:**
- Wrapper script that runs scraper and emails results
- Error notifications via email

**Testing:**
- Run complete workflow manually
- Test failure scenarios
- Verify logs are created

### Phase 3: Scheduling (Essential)

**Tasks:**
- [ ] Set up Windows Task Scheduler task
- [ ] Configure daily schedule (6:00 AM default)
- [ ] Test automated runs
- [ ] Monitor for 1 week
- [ ] Document setup process

**Deliverables:**
- Scheduled task running daily
- Documentation for setup

**Testing:**
- Verify task runs on schedule
- Check email arrives each day
- Monitor for failures

### Phase 4: Security (Important)

**Tasks:**
- [ ] Create `credential_manager.py`
- [ ] Encrypt email passwords
- [ ] Add support for OAuth2 (Gmail)
- [ ] Remove plain-text credentials from config
- [ ] Document security setup

**Deliverables:**
- Secure credential storage
- OAuth2 support for Gmail

**Testing:**
- Verify encrypted credentials work
- Test OAuth2 flow
- Ensure no plain-text passwords

### Phase 5: Advanced Features (Optional)

**Tasks:**
- [ ] Inline HTML email (not just attachment)
- [ ] Multiple recipient support
- [ ] Email template customization
- [ ] Retry mechanism for failed sends
- [ ] Weekly summary report email
- [ ] Delivery confirmation tracking

**Deliverables:**
- Enhanced email features
- Customizable templates
- Summary reports

---

## Configuration Format

### `config_email.yaml` (Example)

```yaml
# Email Delivery Configuration

email:
  enabled: true

  # Delivery schedule (used for reference only, actual scheduling via Task Scheduler/cron)
  schedule: "6:00 AM daily"

  # Email provider
  provider: "gmail"  # Options: gmail, outlook, smtp

  # SMTP Configuration
  smtp:
    server: "smtp.gmail.com"
    port: 587
    use_tls: true

  # Sender information
  sender:
    name: "Healthcare News Scraper"
    email: "your-email@gmail.com"
    # Password stored securely (see credential_manager)

  # Recipients
  recipients:
    - email: "recipient1@example.com"
      name: "Recipient Name"
    - email: "recipient2@example.com"
      name: "Another Recipient"

  # CC/BCC (optional)
  cc: []
  bcc: []

  # Email content
  subject: "Healthcare News Brief - {date}"

  # Delivery method
  delivery:
    method: "attachment"  # Options: attachment, inline, both
    include_summary: true  # Include brief summary in email body

  # Attachments
  attachments:
    - name: "healthcare_brief_{date}.html"
      path: "../briefs/healthcare_brief_google_{date}.html"

  # Error notifications
  error_notification:
    enabled: true
    send_to:
      - "your-email@gmail.com"
    subject: "⚠️ Healthcare News Scraper Failed - {date}"
    include_logs: true

  # Logging
  logging:
    enabled: true
    log_file: "../logs/email_{date}.log"
    keep_logs_days: 30
```

---

## Email Template Design

### Option 1: Attachment Only (Simple)

**Email Body:**
```
Hello,

Your daily Healthcare News Brief is attached.

📊 Summary for [Date]:
- Total Articles: 55
- Top Category: Medicare Advantage Market (11 articles)
- Time Period: Past 7 days

Please open the attached HTML file in your browser to view the full categorized brief.

---
Generated automatically by Healthcare News Scraper
```

### Option 2: Inline HTML (Advanced)

Embed the entire categorized HTML brief directly in the email body.

**Pros:**
- No need to open attachment
- Immediate viewing
- Mobile-friendly

**Cons:**
- Email size larger
- Some email clients may not render perfectly

### Option 3: Hybrid (Recommended)

**Email Body:**
- Brief summary with key metrics
- Top 5 articles (excerpt)
- Link/button to open full HTML attachment

**Attachment:**
- Complete categorized HTML brief

---

## Security Considerations

### Credential Storage

**Option 1: Environment Variables (Simple)**
```bash
export SCRAPER_EMAIL_PASSWORD="your-password"
```

**Option 2: Encrypted Config (Better)**
```python
# Store encrypted password in config
# Decrypt at runtime using master key
```

**Option 3: OAuth2 (Best for Gmail)**
```python
# Use Gmail OAuth2 tokens
# No password needed
# More secure
```

**Option 4: Windows Credential Manager (Windows Only)**
```python
import keyring
keyring.set_password("scraper", "email", "password")
password = keyring.get_password("scraper", "email")
```

### Recommended Approach

**For Gmail:** Use app-specific password (Google Account → Security → App passwords)

**For Enterprise:** Use OAuth2 or SMTP credentials from IT department

---

## Usage After Implementation

### Initial Setup

1. **Configure email settings:**
```bash
nano config_email.yaml
# Add your email, recipients, SMTP settings
```

2. **Set up credentials (Gmail example):**
```bash
# Create app password at https://myaccount.google.com/apppasswords
python src/credential_manager.py --set-password
# Enter your Gmail app password when prompted
```

3. **Test email delivery:**
```bash
./run_scraper_and_email.sh
# Check your inbox for the brief
```

4. **Schedule daily delivery:**
```bash
# Windows: Set up Task Scheduler (see SCHEDULING_GUIDE.md)
# OR
# WSL: Add to crontab
crontab -e
# Add: 0 6 * * * /path/to/run_scraper_and_email.sh
```

### Daily Operation

**Automated:**
- Brief arrives in your inbox every morning at 6:00 AM
- No manual action required

**Manual Run (if needed):**
```bash
./run_scraper_and_email.sh
```

---

## Testing Checklist

### Email Sender Tests
- [ ] Send test email successfully
- [ ] Attachment is readable
- [ ] HTML renders correctly
- [ ] Multiple recipients receive email
- [ ] Error email sent when scraper fails

### Integration Tests
- [ ] Scraper runs and generates brief
- [ ] Email sent automatically after scraper
- [ ] Logs created successfully
- [ ] Error handling works

### Scheduling Tests
- [ ] Task runs at scheduled time
- [ ] Email arrives within 5 minutes of schedule
- [ ] Works when computer is idle/locked
- [ ] Works overnight (Windows sleep settings)

### Security Tests
- [ ] Credentials not visible in logs
- [ ] Config files properly secured
- [ ] OAuth2 flow works (if using)
- [ ] Encrypted passwords decrypt correctly

---

## Success Criteria

✅ **Phase 1-3 (Essential) Complete:**
- [ ] Scraper runs automatically daily at 6:00 AM
- [ ] HTML brief emailed to specified recipients
- [ ] Attachments are readable and well-formatted
- [ ] Error notifications sent when failures occur
- [ ] Logs track all activity

✅ **Phase 4 (Important) Complete:**
- [ ] Email credentials stored securely
- [ ] No plain-text passwords in config files

✅ **Phase 5 (Optional) Complete:**
- [ ] Inline HTML option available
- [ ] Multiple recipient support
- [ ] Weekly summary reports

---

## Estimated Timeline

| Phase | Tasks | Time Estimate |
|-------|-------|---------------|
| Phase 1: Email Core | 5 tasks | 1-2 hours |
| Phase 2: Integration | 5 tasks | 1 hour |
| Phase 3: Scheduling | 5 tasks | 30 minutes |
| Phase 4: Security | 5 tasks | 1 hour |
| Phase 5: Advanced | 6 tasks | 2-3 hours |
| **Total** | **26 tasks** | **5.5-7.5 hours** |

**Recommended: Complete Phases 1-3 first (2.5-3.5 hours) for core functionality**

---

## Dependencies

### Python Libraries Needed

```bash
# Email sending
pip install secure-smtplib

# For Gmail OAuth2 (optional)
pip install google-auth google-auth-oauthlib google-auth-httplib2

# For encryption (if using encrypted credentials)
pip install cryptography

# For keyring integration (optional)
pip install keyring

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Email provider blocks automated sends | High | Use app passwords, OAuth2, or whitelist IP |
| Credentials exposed | High | Use encryption or OAuth2 |
| Task doesn't run when computer asleep | Medium | Configure Windows power settings |
| Email marked as spam | Medium | Configure SPF/DKIM, use proper From address |
| Attachment too large | Low | Compress HTML or use inline delivery |

---

## Next Steps

1. **Review this feature request**
2. **Decide on priority (Essential phases or all phases)**
3. **Approve implementation**
4. **Begin Phase 1 development**

---

## Questions to Answer Before Implementation

1. **Which email provider will you use?**
   - Gmail (personal)
   - Outlook/Office 365 (work)
   - Custom SMTP server

2. **Who should receive the brief?**
   - Just you
   - Team members
   - Multiple distribution lists

3. **Preferred delivery method?**
   - Attachment only (simple, recommended)
   - Inline HTML (fancy, may have rendering issues)
   - Both

4. **What time should it run?**
   - 6:00 AM (recommended)
   - 7:00 AM
   - Custom time

5. **How should credentials be stored?**
   - App password (Gmail, simple)
   - OAuth2 (Gmail, more secure)
   - Environment variables
   - Encrypted config file

---

**Status:** 📋 Ready for Development
**Ready to implement?** Reply with your answers to the questions above and we'll build this feature!
