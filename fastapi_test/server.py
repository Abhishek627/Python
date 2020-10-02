from fastapi import FastAPI, Body
from base_models import *


# Initialising an object FastAPI
app = FastAPI()


# Boilerplate for get request; change
# the endpoint according to your needs
@app.get("/get_test")
# Add or remove the async depending
# on the kind of server you are looking
# to build
async def root():
    return {
        "success": True,
        "message": "Boilerplate code to get started with FastAPI",
        "data": {}
    }

# Boilerplate for post request; change
# the endpoint according to your needs


@app.post("/post_test")
# The PostIn is the type of the body
# that is sent as a post request to this
# endpoint; you can do any kind of manipulations
# to the data and then return it either as
# a straighforward JSON or via a model
# similar to what I have created
def eval(post_in: PostIn):
    return {
        "success": True,
        "message": "Code successfully evaluated by the interpreter.",
        "data": PostOut(out=post_in.inp)
    }
