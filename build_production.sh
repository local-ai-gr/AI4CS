#!/bin/bash

# Set the name or ID of the container you want to target
CONTAINER_NAME_OR_ID="app-dev-container"

# Set the path of the source folder inside the container (the one you want to copy files from)
SOURCE_PATH="/usr/src/app/.output/public"

# Set the path of the destination folder on your host machine
DESTINATION_PATH="./ai4cs-prod"

# Run the 'npm run generate' command inside the container
docker exec -it $CONTAINER_NAME_OR_ID npm run generate

# Copy the files from the container's .output folder to the host's production_build folder
docker cp $CONTAINER_NAME_OR_ID:$SOURCE_PATH/. $DESTINATION_PATH

docker restart -t 5 $CONTAINER_NAME_OR_ID

echo "Operation completed. Files have been copied to $DESTINATION_PATH."