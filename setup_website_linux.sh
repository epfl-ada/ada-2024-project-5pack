#!/bin/bash

echo "Setting up Jekyll for Linux..."

# Install Ruby and development tools
if ! command -v ruby &> /dev/null; then
    echo "Installing Ruby and development tools..."
    sudo apt-get update
    sudo apt-get install -y ruby-full build-essential zlib1g-dev
fi

# Add local gem location to path
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install bundler if not installed
if ! command -v bundle &> /dev/null; then
    echo "Installing Bundler..."
    gem install bundler
fi

# Install Jekyll and dependencies
echo "Installing Jekyll and dependencies..."
cd data_story
bundle install

echo "Setup complete! You can now run the website locally with:"
echo "cd data_story"
echo "bundle exec jekyll serve"
