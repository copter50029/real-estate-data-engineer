# Scrapling Setup Guide

This guide will help you set up a Python virtual environment and install scrapling for web scraping.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Step 1: Create a Virtual Environment

Navigate to your project directory and create a virtual environment:

```bash
# Create a virtual environment named .venv
python3 -m venv .venv
```

## Step 2: Activate the Virtual Environment

### On Linux/Mac:
```bash
source .venv/bin/activate
```

### On Windows:
```bash
.venv\Scripts\activate
```

You should see `(.venv)` prefix in your terminal prompt, indicating the virtual environment is active.

## Step 3: Install Scrapling

Install scrapling with fetchers support (includes playwright and patchright):

```bash
pip install "scrapling[fetchers]"
```

## Step 4: Install Playwright Browsers

After installing scrapling, you need to install the browser binaries:

```bash
scrapling install
```

This command will:
- Install Playwright browsers (Chromium, Firefox, WebKit)
- Install necessary system dependencies
- May require sudo password for system dependencies

## Step 5: Install All Scrapling Features (Optional)

For full functionality including MCP support and additional features:

```bash
pip install "scrapling[all]"
```

## Verify Installation

Test that everything is installed correctly:

```bash
python -c "from scrapling import Fetcher; print('Scrapling installed successfully!')"
```

## Running the Scraper

Once everything is installed, you can run the scraper:

```bash
python scraper.py
```

## Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

### Permission Issues
If you encounter permission issues during `scrapling install`, make sure to enter your sudo password when prompted.

### Browser Installation Issues
If browsers fail to install, try:
```bash
playwright install
playwright install-deps
```

### Missing Dependencies
If you get import errors, ensure all dependencies are installed:
```bash
pip install "scrapling[all]"
```