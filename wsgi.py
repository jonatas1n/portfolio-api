from fastapi import FastAPI
from mangum import Mangum

from main import app  

handler = Mangum(app)
