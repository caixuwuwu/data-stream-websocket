#!/bin/sh
CMD=${1-up}
echo "Command: $CMD"
if [ "$CMD" == 'build' ]; then
    docker-compose -f docker/docker-compose-build.yml up build-data-stream-websocket
    docker-compose -f docker/docker-compose-build.yml down
elif [ "$CMD" == 'rebuild' ]; then
    ./dev.sh down
    [ ! -z $(docker images -q data_stream_websocket) ] && docker rmi data_stream_websocket
    ./dev.sh build
elif [ "$CMD" == 'down' ]; then
    docker-compose -f docker/docker-compose.yml down
elif [ "$CMD" == 'up' ]; then
    docker-compose -f docker/docker-compose.yml up
elif [ "$CMD" == 'unittest' ]; then
    docker-compose -f docker/docker-compose-ut.yml up
    docker-compose -f docker/docker-compose-ut.yml down
elif [ "$CMD" == 'clear' ]; then
    if [ ! -z $(docker ps -a -q -f name=data_stream_websocket) ]; then
        docker-compose -f docker/docker-compose-build.yml down
        docker-compose -f docker/docker-compose.yml down
        docker stop $(docker ps -a -q -f name=data_stream_websocket)
        docker rm $(docker ps -a -q -f name=data_stream_websocket)
    fi
elif [ "$CMD" == 'deploy' ]; then
    TAG=$2
    if [ "$TAG" == '' ]; then
        echo "empty tag!"
    else
        echo "tag: $TAG"
        git tag -d $TAG
        git tag $TAG
        git push origin $TAG
    fi
fi
