#!/usr/bin/env python
import gzip
import json

import pysolr
import click

SOLR_URL = "http://solr:8983/solr/wikipedia"
USED_FIELDS = [
    "description",
    "highlights",
    "id",
    "lang",
    "links",
    "lists",
    "paragraphs",
    "sections",
    "timestamp",
    "title",
    "type",
]


@click.group()
def cli():
    pass


def parse_article(line):
    article = json.loads(line)
    if article["type"] == "REDIRECT":
        return None
    article["id"] = article["wid"]
    if "paragraphs" in article and len(article["paragraphs"]) > 0:
        article['description'] = article['paragraphs'][0]
    if "links" in article:
        links = []
        for link in article["links"]:
            links.append(link["description"])
        article["links"] = links    
    for field in list(article.keys()):
        if field not in USED_FIELDS:
            del article[field]
    return article


@cli.command("delete")
def delete_existing_index():
    solr = pysolr.Solr(SOLR_URL, timeout=10)
    click.echo("Deleting existing index...")
    solr.delete("*:*")
    solr.commit()


@cli.command("index")
@click.option("--input", type=click.Path(), required=True)
@click.option("--commit-freq", default=1000, type=int)
def index_collection(input, commit_freq):
    solr = pysolr.Solr(SOLR_URL, timeout=10)
    click.echo("Starting indexing data...")
    with gzip.open(input, "r") as finput:
        articles = []
        for line in finput:
            article = parse_article(line)
            if article:
                articles.append(article)
            if len(articles) % commit_freq == 0:
                solr.add(articles)
                solr.commit()
                articles = []
        solr.add(articles)
        solr.commit()


if __name__ == "__main__":
    cli()