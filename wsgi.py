from fastapi import FastAPI
from main import app

def application(scope):
    return app(scope)
