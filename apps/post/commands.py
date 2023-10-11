import click

from apps.post.app import app

from flask import Flask

@app.cli.command("create-base-bucket")
def create_base_bucket():
    pass
