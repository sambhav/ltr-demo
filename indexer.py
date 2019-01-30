#!/usr/local/bin/python
import gzip
import json
import re
from concurrent.futures import ProcessPoolExecutor

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
    "wikiTitle",
]

TEMPLATE_PATTERN = re.compile(r"TEMPLATE\[.*\]", flags=re.M)


@click.group()
def cli():
    pass


def parse_article(line):
    article = json.loads(line)
    if article["type"] == "REDIRECT":
        return None
    article["id"] = article["wid"]
    if "paragraphs" in article and len(article["paragraphs"]) > 0:
        article["description"] = re.sub(TEMPLATE_PATTERN, "", article["paragraphs"][0])
    if "links" in article:
        links = []
        for link in article["links"]:
            links.append(link["anchor"])
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


def process_articles(articles):
    solr = pysolr.Solr(SOLR_URL, timeout=10)
    processed_articles = filter(bool, map(parse_article, articles))
    solr.add(processed_articles)


@cli.command("index")
@click.option("--input", type=click.Path(), required=True)
@click.option("--post-freq", default=1000, type=int)
def index_collection(input, post_freq):
    with gzip.open(input, "r") as finput:
        click.echo("Reading input file...")
        articles = finput.readlines()
        click.echo("Input loaded.")
        click.echo("Document indexing in progress...")
        article_chunks = [
            articles[i : i + post_freq] for i in range(0, len(articles), post_freq)
        ]
        with ProcessPoolExecutor(max_workers=4) as executor:
            with click.progressbar(
                executor.map(process_articles, article_chunks),
                length=len(article_chunks),
            ) as tasks:
                # Iterating through the tasks just to execute them
                for task in tasks:
                    pass


if __name__ == "__main__":
    cli()
