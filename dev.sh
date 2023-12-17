#docker build . -t freetar
#docker run -p 8080:8080 freetar

mkdir -p data
docker-compose  -f deployment/dev.yml build
docker-compose  -f deployment/dev.yml up