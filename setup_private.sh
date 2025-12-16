#!/bin/bash

# Define the path to the config directory and the .env file
CONFIG_DIR="config"
ENV_FILE=".env"

# Create the config directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating directory: $CONFIG_DIR"
    mkdir "$CONFIG_DIR"
else
    echo "Directory $CONFIG_DIR already exists."
fi

# Change to the config directory
cd "$CONFIG_DIR" || exit

# Check if the .env file already exists
if [ -f "$ENV_FILE" ]; then
    echo "$ENV_FILE already exists. Overwriting..."
else
    echo "$ENV_FILE does not exist. Creating a new one..."
fi

# Write the data into the .env file
echo "USER_AGENT='user agent'" > "$ENV_FILE"

echo ".env file created successfully with data:"
cat "$ENV_FILE"

