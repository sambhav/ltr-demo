#!/usr/bin/env python
import click
from flaskapp import app
from flaskapp.models import utils, ranklib, linear
from flaskapp.query import get_rankers


@click.group()
def cli():
    pass


@cli.command("run-server", help="Run the web UI server.")
def run_server():
    app.run(host="0.0.0.0")


def _train_and_upload_model(model):
    model.train()
    click.echo("Training finished. Uploading model to Solr...")
    utils.upload_model(model.name, model.to_json())
    click.echo("Done")


@cli.group(help="Train and upload machine-learned models to Solr.")
def train():
    pass


@train.command("linear", help="Train and upload a linear model to Solr.")
def train_linear():
    click.echo(f"Training a linear model")
    model = linear.LinearModel()
    _train_and_upload_model(model)


@train.command("lambdamart", help="Train and upload a LambdaMart model to Solr.")
@click.option(
    "-n",
    "--number-of-trees",
    "num_trees",
    type=int,
    default=100,
    help="Number of trees in the final model.",
)
@click.option(
    "-m",
    "--metric",
    type=click.Choice(["P", "NDCG", "RR", "ERR", "DCG"]),
    default="NDCG",
    help="Metric to optimize.",
)
@click.option("-k", type=int, default=10)
def train_lambdamart(num_trees, metric, k):
    click.echo(
        f"Training a LambdaMart model with parameters - Trees: {num_trees} Metric: {metric}@{k}"
    )
    model = ranklib.LambdaMartModel(num_trees, metric, k)
    _train_and_upload_model(model)


@cli.command("delete-model", help="Delete user loaded models from Solr.")
@click.option(
    "--name",
    type=click.Choice(get_rankers(default=False)),
    required=False,
    default=None,
    help="Name of the model you want to delete.",
)
@click.option(
    "-a",
    "--all-models",
    "delete_all",
    is_flag=True,
    help="Delete all models uploaded on Solr except the default ranker.",
)
def delete_model(name, delete_all):
    if delete_all:
        if click.confirm("Are you sure you want to delete all models?"):
            click.echo("Deleting all models...")
            utils.delete_all_models()
    elif name:
        click.echo(f"Deleteing {name}")
        utils.delete_model(name)
    else:
        raise click.UsageError(
            "Either specify a model name or pass the --all-models flag to delete all models"
        )
    click.echo("Done")


if __name__ == "__main__":
    cli()
