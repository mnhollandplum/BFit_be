from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the BFit API. Check out our Github for instructions on accessing our endpoints"
