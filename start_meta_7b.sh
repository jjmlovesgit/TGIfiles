#!/bin/bash

#Start up for running Local off the Internet for Demo 9/22/23
#Copy this to where you cloned the text-generation-inforence files

# Variables
model="Llama-2-7b-chat"
volume="$PWD/data"

# Echo starting message
echo "Starting the Docker container with local files (No Internet): $model and volume: $volume ..."

# Start the Docker container
docker run --rm --entrypoint /bin/bash -itd \
  --name $model \
  -v $volume:/data \
  --gpus all -p 8080:80 ghcr.io/huggingface/text-generation-inference:latest

# Check if the container started successfully
if [ $? -eq 0 ]; then
    echo "Container started successfully!"
else
    echo "Failed to start the container."
    exit 1
fi

# Echo running the launcher message
echo "Running the text-generation-launcher command from /data directory inside the container...Local Files only will be used"
docker exec $model bash -c "text-generation-launcher --model-id /data/$model --num-shard 1"

# Check if the text-generation-launcher command was successful
if [ $? -eq 0 ]; then
    echo "text-generation-launcher ran successfully!"
else
    echo "Failed to run text-generation-launcher."
    exit 1
fi
