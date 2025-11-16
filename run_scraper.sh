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
