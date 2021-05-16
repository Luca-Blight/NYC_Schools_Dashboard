import sys
from flask import Flask
from test_project.backend.src.adapters.builder import ParentBuilder
from test_project.backend.src.entrypoints.app import create_app,FlaskGroup

app = create_app()
cli = FlaskGroup(create_app=create_app)

school_run = ParentBuilder().school_run()
attn_run = ParentBuilder().attn_run()
pop_run = ParentBuilder().pop_run()
scores_run = ParentBuilder().scores_run() 

if __name__ == "__main__":
    cli()
