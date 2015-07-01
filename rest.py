from flask import Flask
import datastore

app = Flask(__name__)


@app.route('/')
def status():
    return 'Status of all to-do lists will go here'


@app.route('/<list_name>', methods=['POST'])
def create_list(list_name):
    pass


@app.route('/<list_name>', methods=['PATCH'])
def update_list(list_name):
    pass


@app.route('/<list_name>', methods=['DELETE'])
def delete_list(list_name):
    pass


if __name__ == '__main__':
    app.run(9080, debug=True)
