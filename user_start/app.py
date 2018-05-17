from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template("index.html")


class Caller:
    def __init__(self, address: str):
        self.address = address

    def get(self, address: str):
        return requests.get(self.address + address).json()


competency_manager = Caller('http://127.0.0.1:5001')
labor_manager = Caller('http://127.0.0.1:5002')


@app.route('/demanded_competencies')
def demanded_competencies():
    competencies_ids = labor_manager.get('/demanded_competencies')
    competencies = [competency_manager.get('/competencies/%d' % competency_id) for competency_id in competencies_ids]
    return render_template("demanded_competencies.html", competencies=competencies)


if __name__ == '__main__':
    app.run(port=5000)
