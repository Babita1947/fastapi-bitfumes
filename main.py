from fastapi import FastAPI

app = FastAPI() # instance of FastAPI


@app.get('/')
def index():
    return {'data': {'name':'Sarthak'}}

@app.get('/about')
def about():
    return {'data': 'about page'}