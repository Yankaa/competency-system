from flask import Flask
import downloader
import parser
import analyzer

app = Flask(__name__)


@app.route('/update')
def hello_world():
    fresh_standards = downloader.update()
    parser.convert(fresh_standards)
    analyzer.analyze(fresh_standards)
    return 'Updated'


if __name__ == '__main__':
    app.run(port=5004)
