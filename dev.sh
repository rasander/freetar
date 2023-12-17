#docker build . -t freetar
#docker run -p 8080:8080 freetar

mkdir -p data
docker compose build
sleep 1
docker compose up