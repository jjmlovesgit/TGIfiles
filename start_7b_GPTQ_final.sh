#Two stage startup - Runs with or without Internet requires previously downloaded model
#requires previously downloaded model
#Step 1 - copy this script to your text-generation-inference dir
#Step 2 - from "text-generation-inference dir/data" sudo git clone https://huggingface.co/TheBloke/Llama-2-7b-Chat-GPTQ
#step 3 - Retrun to text-generation-inference dir
#step 4 - Run startup script

#!/bin/bash

# Variables
model="Llama-2-7b-Chat-GPTQ"
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

# Run text-generation-launcher lauch command from inside the container for finer control over the container's execution environment
echo "Running the text-generation-launcher command from /data directory inside the container...Local Files only will be used"
docker exec $model bash -c "text-generation-launcher --model-id /data/$model --quantize gptq --num-shard 1"

# Check if the text-generation-launcher command was successful
if [ $? -eq 0 ]; then
    echo "text-generation-launcher ran successfully!"
else
    echo "Failed to run text-generation-launcher."
    exit 1
fi
