docker build \
    -f main.Dockerfile \
    -t jonk_bot_image .
docker run -d \
    --name jonk_bot \
    jonk_bot_image
