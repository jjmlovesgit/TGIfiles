while true; do
    if curl -IsSf http://www.cnn.com >/dev/null; then
        spaces=$((1 + RANDOM % 5))  # Generate a random number between 1 and 5
        echo -n "Internet is working."
        for ((i=0; i<spaces; i++)); do
            echo -n " "
        done
        echo "Internet is working."
    else
        spaces=$((1 + RANDOM % 5))  # Generate a random number between 1 and 5
        echo -n "Internet is down."
        for ((i=0; i<spaces; i++)); do
            echo -n " "
        done
        echo "Internet is down."
    fi
    sleep 1  # Adjust the interval (in seconds) as needed
done