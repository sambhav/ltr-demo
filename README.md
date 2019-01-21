# LTR-demo

This repository is supposed to serve as a demo of Learning-to-Rank for Solr.

## Building the demo

This demo requires you to have docker and docker compose installed. Follow the instructions on the
[official docker docs page](https://docs.docker.com/compose/install/) carefully to install docker-compose
for your OS. Once that is installed -

1. Checkout this git repository locally and `cd` to the root of this repo.
2. Download the wikipedia dump -
```
wget https://github.com/samj1912/ltr-demo/releases/download/data-dump/simple-wikipedia.json.gz
```
3. Run the following commands to bring up an instance of Solr up with the required config -
```
docker-compose build
docker-compose up -d solr
```
4. To index the above dump run
```
docker-compose up indexer
```

## Annotations and Training

// TODO
