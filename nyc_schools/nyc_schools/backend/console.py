import sys
from flask.cli import FlaskGroup
from api.src import create_app,adapters

# from .api.src import db

school_run = adapters.ParentBuilder().school_run()
attn_run = adapters.ParentBuilder().attn_run()
pop_run = adapters.ParentBuilder().pop_run()
scores_run = adapters.ParentBuilder().scores_run()


app = create_app()
cli = FlaskGroup(create_app=app)


if __name__ == "__main__":
    cli()
