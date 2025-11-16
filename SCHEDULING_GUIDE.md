# Scheduling Guide - Auto-Run Daily Brief

**Goal:** Automatically run the healthcare news scraper at a specific time each day

---

## Option 1: WSL Cron (Recommended for Linux Users)

### Pros
- Native Linux scheduling
- Runs in WSL environment
- Most reliable for WSL-based scripts

### Cons
- WSL must be running at scheduled time
- Windows may suspend WSL when idle

### Setup Instructions

1. **Ensure cron is installed in WSL:**
```bash
sudo apt-get update
sudo apt-get install cron
```

2. **Start cron service:**
```bash
sudo service cron start
```

3. **Create a wrapper script:**
```bash
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper
nano run_scraper.sh
```

Add this content:
```bash
#!/bin/bash
# Healthcare News Scraper - Daily Run Script
# This script runs the scraper and logs results

# Set working directory
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/briefs

# Set log file with date
LOG_FILE="../logs/scraper_$(date +%Y-%m-%d).log"

# Create logs directory if it doesn't exist
mkdir -p ../logs

# Run scraper and capture output
echo "===========================================" >> "$LOG_FILE"
echo "Starting scraper at $(date)" >> "$LOG_FILE"
echo "===========================================" >> "$LOG_FILE"

../venv/bin/python ../src/scraper_google.py >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    echo "✓ Scraper completed successfully at $(date)" >> "$LOG_FILE"
else
    echo "✗ Scraper failed at $(date)" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
```

4. **Make script executable:**
```bash
chmod +x run_scraper.sh
```

5. **Test the script:**
```bash
./run_scraper.sh
```

6. **Edit crontab:**
```bash
crontab -e
```

7. **Add this line to run daily at 6:00 AM:**
```bash
0 6 * * * /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/run_scraper.sh
```

**Cron Schedule Examples:**
```bash
# Every day at 6:00 AM
0 6 * * * /path/to/run_scraper.sh

# Every day at 8:30 AM
30 8 * * * /path/to/run_scraper.sh

# Every day at 9:00 PM
0 21 * * * /path/to/run_scraper.sh

# Monday-Friday at 7:00 AM
0 7 * * 1-5 /path/to/run_scraper.sh
```

8. **Verify crontab is set:**
```bash
crontab -l
```

**Important:** WSL must be running for cron to execute. See Option 3 for keeping WSL alive.

---

## Option 2: Windows Task Scheduler (Recommended for Windows Users)

### Pros
- Native Windows solution
- Runs even when you're not logged in
- Reliable on Windows systems
- Visual interface

### Cons
- More complex setup
- Need to handle WSL startup

### Setup Instructions

1. **Create a Windows batch file:**

Open Notepad and create: `C:\Scripts\run_healthcare_scraper.bat`

```batch
@echo off
REM Healthcare News Scraper - Windows Task Scheduler Script

REM Log file with date
set LOGFILE=C:\Users\17342\OneDrive\Claude Code\Code\news_scraper\logs\scraper_%date:~-4,4%-%date:~-10,2%-%date:~-7,2%.log

REM Create logs directory if it doesn't exist
if not exist "C:\Users\17342\OneDrive\Claude Code\Code\news_scraper\logs" mkdir "C:\Users\17342\OneDrive\Claude Code\Code\news_scraper\logs"

REM Run scraper in WSL
echo ========================================== >> "%LOGFILE%"
echo Starting scraper at %date% %time% >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"

wsl -d Ubuntu -e bash -c "cd '/mnt/c/Users/17342/OneDrive/Claude Code/Code/news_scraper/briefs' && ../venv/bin/python ../src/scraper_google.py" >> "%LOGFILE%" 2>&1

if %errorlevel% equ 0 (
    echo Success: Scraper completed at %date% %time% >> "%LOGFILE%"
) else (
    echo Error: Scraper failed at %date% %time% >> "%LOGFILE%"
)

echo. >> "%LOGFILE%"
```

2. **Test the batch file:**
- Double-click `run_healthcare_scraper.bat`
- Check that it runs successfully

3. **Open Windows Task Scheduler:**
- Press `Windows + R`
- Type `taskschd.msc`
- Press Enter

4. **Create a New Task:**
- Click "Create Task" (not "Create Basic Task")
- Name: "Healthcare News Scraper Daily"
- Description: "Runs healthcare news scraper daily at 6 AM"
- Check "Run whether user is logged on or not"
- Check "Run with highest privileges"

5. **Set Trigger:**
- Go to "Triggers" tab
- Click "New"
- Begin the task: "On a schedule"
- Settings: "Daily"
- Start time: 06:00:00 AM
- Recur every: 1 days
- Click OK

6. **Set Action:**
- Go to "Actions" tab
- Click "New"
- Action: "Start a program"
- Program/script: `C:\Scripts\run_healthcare_scraper.bat`
- Click OK

7. **Configure Settings:**
- Go to "Settings" tab
- Check "Allow task to be run on demand"
- Check "Run task as soon as possible after a scheduled start is missed"
- Uncheck "Stop the task if it runs longer than"
- Click OK

8. **Test the Task:**
- Right-click the task
- Click "Run"
- Check the log file to verify it worked

---

## Option 3: Keep WSL Running (For Cron Reliability)

If using WSL cron, you need to ensure WSL stays running.

### Method A: WSL Configuration (Windows 11)

Create/edit `C:\Users\17342\.wslconfig`:

```ini
[wsl2]
# Keep WSL running even when all sessions are closed
autoShutdown=false

# Set memory limit (optional)
memory=4GB
```

Then restart WSL:
```bash
wsl --shutdown
wsl
```

### Method B: Background Task

Create a simple batch file that keeps WSL alive:

`C:\Scripts\keep_wsl_alive.bat`
```batch
@echo off
:loop
wsl -d Ubuntu -e echo "Keep alive ping" > nul
timeout /t 3600 /nobreak > nul
goto loop
```

Schedule this to run at Windows startup in Task Scheduler.

---

## Option 4: Python Scheduler (Alternative)

If you prefer a pure Python solution, you can use `schedule` library.

### Setup

1. **Install schedule:**
```bash
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper
source venv/bin/activate
pip install schedule
```

2. **Create scheduler script:**

`src/scheduler.py`:
```python
#!/usr/bin/env python3
"""
Daily Scheduler for Healthcare News Scraper
Runs the scraper at a specified time each day
"""
import schedule
import time
import subprocess
import os
from datetime import datetime

def run_scraper():
    """Run the healthcare news scraper"""
    print(f"\n{'='*70}")
    print(f"Running scraper at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    # Change to briefs directory
    os.chdir('/mnt/c/Users/17342/OneDrive/Claude Code/Code/news_scraper/briefs')

    # Run scraper
    try:
        result = subprocess.run(
            ['../venv/bin/python', '../src/scraper_google.py'],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        print(result.stdout)

        if result.returncode == 0:
            print(f"\n✓ Scraper completed successfully at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"\n✗ Scraper failed with error code {result.returncode}")
            print(result.stderr)

    except subprocess.TimeoutExpired:
        print("\n✗ Scraper timed out after 10 minutes")
    except Exception as e:
        print(f"\n✗ Error running scraper: {str(e)}")

# Schedule the scraper to run daily at 6:00 AM
schedule.every().day.at("06:00").do(run_scraper)

print("Healthcare News Scraper Scheduler Started")
print("Scheduled to run daily at 6:00 AM")
print("Press Ctrl+C to stop\n")

# Optional: Run once immediately on startup
# run_scraper()

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

3. **Make executable:**
```bash
chmod +x src/scheduler.py
```

4. **Test it:**
```bash
cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper
venv/bin/python src/scheduler.py
```

5. **Run in background (WSL):**
```bash
nohup venv/bin/python src/scheduler.py > logs/scheduler.log 2>&1 &
```

6. **Or schedule it to start at boot using cron:**
```bash
@reboot cd /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper && nohup venv/bin/python src/scheduler.py > logs/scheduler.log 2>&1 &
```

---

## Recommended Approach

### For Most Users: **Windows Task Scheduler (Option 2)**

**Why:**
- Native Windows solution
- Reliable and tested
- Runs even when not logged in
- Visual interface for management
- No need to keep WSL running 24/7

**Quick Setup:**
1. Create `C:\Scripts\run_healthcare_scraper.bat` (see Option 2)
2. Set up Windows Task Scheduler task
3. Set schedule (e.g., daily at 6:00 AM)
4. Test by right-clicking and selecting "Run"

### For Advanced Linux Users: **WSL Cron (Option 1)**

**Why:**
- Native Linux scheduling
- Familiar cron syntax
- Integrated with WSL environment

**Considerations:**
- Must keep WSL running (use Option 3)
- May not work if Windows suspends WSL

---

## Monitoring & Logs

### Check Logs

**Option 1/2 (Script-based):**
```bash
# View today's log
cat /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/logs/scraper_$(date +%Y-%m-%d).log

# View recent logs
ls -lt /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/logs/ | head -10
```

**Option 4 (Python scheduler):**
```bash
# View scheduler log
tail -f /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/logs/scheduler.log
```

### Verify Task Ran

**Windows Task Scheduler:**
- Open Task Scheduler
- Click "Task Scheduler Library"
- Find "Healthcare News Scraper Daily"
- Check "Last Run Result" (should be 0x0 for success)
- Check "Last Run Time"

**WSL Cron:**
```bash
# Check cron is running
sudo service cron status

# View cron logs (may need to enable)
grep CRON /var/log/syslog | tail -20
```

### Check Output Files

```bash
# List recent briefs
ls -lt /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/briefs/*.html | head -5

# Verify today's brief exists
ls -lh /mnt/c/Users/17342/OneDrive/Claude\ Code/Code/news_scraper/briefs/healthcare_brief_google_$(date +%Y-%m-%d).html
```

---

## Troubleshooting

### Task Didn't Run

**Windows Task Scheduler:**
1. Check Task Scheduler history
2. Verify task is "Ready" not "Disabled"
3. Check if computer was awake at scheduled time
4. Review log file for errors

**WSL Cron:**
1. Check if cron is running: `sudo service cron status`
2. Check if WSL was running at scheduled time
3. Verify crontab entry: `crontab -l`
4. Check syslog: `grep CRON /var/log/syslog`

### Script Failed

1. **Check log file** for error messages
2. **Test manually** by running the script
3. **Verify paths** are correct (spaces escaped)
4. **Check permissions** on scripts and directories
5. **Verify venv** is working: `venv/bin/python --version`

### No Brief Generated

1. Check if scraper ran (check logs)
2. Check if Google News is accessible
3. Verify internet connection was active
4. Check for errors in log file

---

## Summary

| Method | Difficulty | Reliability | Platform | Recommendation |
|--------|-----------|-------------|----------|----------------|
| Windows Task Scheduler | Medium | ⭐⭐⭐⭐⭐ | Windows | ✅ **Best for most users** |
| WSL Cron | Easy | ⭐⭐⭐ | WSL | Good if you keep WSL running |
| Python Scheduler | Easy | ⭐⭐⭐ | Both | Good for testing |
| Keep WSL Alive | Medium | ⭐⭐⭐⭐ | WSL | Required for cron reliability |

---

## Next Steps

1. Choose your preferred scheduling method
2. Follow the setup instructions
3. Test the scheduled task manually
4. Verify log files are being created
5. Check that briefs are generated on schedule
6. Set up monitoring (optional)

---

**Recommended: Windows Task Scheduler at 6:00 AM daily**

This will give you fresh healthcare news every morning when you start work!
