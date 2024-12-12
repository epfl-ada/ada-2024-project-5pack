# Windows PowerShell script for setting up Jekyll

# Check if Ruby is installed
if (!(Get-Command ruby -ErrorAction SilentlyContinue)) {
    Write-Host "Ruby is not installed. Please:"
    Write-Host "1. Download RubyInstaller with DevKit from https://rubyinstaller.org/downloads/"
    Write-Host "2. Run the installer and make sure to select 'Add Ruby executables to your PATH'"
    Write-Host "3. Run this script again after installing Ruby"
    Exit
}

# Check Ruby version
$rubyVersion = ruby -v
Write-Host "Using Ruby version: $rubyVersion"

# Install bundler if not installed
if (!(Get-Command bundle -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Bundler..."
    gem install bundler
}

# Install Jekyll and dependencies
Write-Host "Installing Jekyll and dependencies..."
Set-Location data_story
bundle install

Write-Host ""
Write-Host "Setup complete! You can now run the website locally with:"
Write-Host "cd data_story"
Write-Host "bundle exec jekyll serve"
