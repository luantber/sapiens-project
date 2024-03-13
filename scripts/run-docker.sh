docker rm -f iris
docker run -p 80:80 -v ${HOME}/.config/gcloud:/root/.config/gcloud --name iris iris_server 