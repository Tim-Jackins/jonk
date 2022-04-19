docker build \
    -f Dockerfile \
    -t jonk_bot_image .
docker run -d \
    --name jonk_bot \
    jonk_bot_image
