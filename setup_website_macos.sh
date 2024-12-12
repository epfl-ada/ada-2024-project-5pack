#!/bin/bash

echo "Setting up Jekyll for macOS..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Ruby if not installed
if ! command -v ruby &> /dev/null; then
    echo "Installing Ruby..."
    brew install ruby
fi

# Add Ruby to PATH (needed for newly installed Ruby)
echo 'export PATH="/usr/local/opt/ruby/bin:/usr/local/lib/ruby/gems/3.0.0/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

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
