docker build -t python_crawler .
docker run -d -it --name crawler -p 8082:8082 -v /$(pwd):/crawler -v /$(pwd)/cron:/etc/cron.d/cron python_crawler
docker network connect crawler_default crawler