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
4. Solr will then be reachable on `http://localhost:8983/solr`
4. To index the above dump run
```
docker-compose up indexer
```
5. To bring up the web app for annotations and model comparisons run -
```
docker-compose up -d webapp
```
6. The web app will be available on `http://localhost:5000`

## Annotations and Training

1. You can use the page at `http://localhost:5000` to annotate queries, just type a query and mark the documents as relevant/not relevant (just click on the button next to each result to flip it).

2. Once that you have your annotations, you can check the performance of the solr baseline model (bm25) by visiting `http://localhost:5000/stats`, if you click on the model name you will see more detail about the performance of the model - and how the model is ranking each single query. 

3. Let's train a model now: 
```
docker exec ltr-demo_webapp_1 ./manage.py train 
```
To get a help page describing different ways to train a model. 

4. To train and upload a linear model to Apache Solr execute: 
```
docker exec ltr-demo_webapp_1 ./manage.py train linear
```
It will train and upload a linear model - once you run it, you can visit `http://localhost:5000/stats` and see the new model. 

5. To train and upload a tree model to Apache Solr execute: 
```
docker exec ltr-demo_webapp_1 ./manage.py train lambdamart 
```
It will train and upload a tree model - once you run it, you can visit `http://localhost:5000/stats` and see the new model. 
You can customize the training parameters for the lambdamart model, you can find more details in:

```
docker exec ltr-demo_webapp_1 ./manage.py train lambdamart --help
```

