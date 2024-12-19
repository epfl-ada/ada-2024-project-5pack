# Website Setup Instructions

This document explains how to set up and run the data story website locally.

## Prerequisites

You'll need git and Python with Poetry already installed (see main README.md for project setup).

## Setup Instructions

### For macOS:
```bash
# Make the script executable
chmod +x setup_website_macos.sh
# Run the setup script
./setup_website_macos.sh
```

### For Linux:
```bash
# Make the script executable
chmod +x setup_website_linux.sh
# Run the setup script
./setup_website_linux.sh
```

### For Windows:
```powershell
# Run the setup script in PowerShell
.\setup_website_windows.ps1
```

If you encounter any issues with the Windows setup:
1. Download RubyInstaller with DevKit from https://rubyinstaller.org/downloads/
2. Run the installer and select 'Add Ruby executables to your PATH'
3. Run the setup script again

## Running the Website

After setup is complete, you can run the website locally:
```bash
cd data_story
bundle exec jekyll serve
```
The website will be available at http://localhost:4000

## Generating Content

To generate new plots for the website:
```bash
poetry run python -m src.scripts.data_story.generate_plots
```

## Project Structure

The website-related files are organized as follows:
```
project_root/
├── data_story/              # Website content
│   ├── _config.yml         # Jekyll configuration
│   ├── index.md           # Main content
│   └── assets/
│       └── plots/         # Generated plots
├── src/
│   └── scripts/
│       └── data_story/    # Plot generation scripts
│           ├── plots/     # Individual plot modules
│           │   ├── network_plots.py
│           │   ├── path_analysis.py
│           │   └── player_stats.py
│           └── generate_story.py
```

## Common Issues

### Ruby Version Issues
If you get Ruby version-related errors:
- On macOS: Try `brew upgrade ruby`
- On Linux: Try `sudo apt-get update && sudo apt-get upgrade ruby-full`

### Jekyll Build Errors
If Jekyll fails to build:
1. Delete the Gemfile.lock file
2. Run `bundle install` again
3. Try running Jekyll again
