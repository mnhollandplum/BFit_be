from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Welcome to BFit API</h1>"

if __name__ == '__main__':
  app.run(debug=True)
