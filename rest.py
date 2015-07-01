from flask import Flask, jsonify, Response, redirect, url_for, request
from datastore import Database
from webargs.flaskparser import use_args, use_kwargs, FlaskParser
from webargs import Arg

app = Flask(__name__)
db = Database()
parser = FlaskParser()


@app.route('/')
def main():
    return redirect(url_for('lists'))


@app.route('/lists')
def lists():
    all_lists = db.list_all()
    response = jsonify(all_lists)
    response.status_code = 200 if len(all_lists) > 0 else 404
    return response


@app.route('/lists/create', methods=['POST'])
@use_args({'name': Arg(str, required=True, validate=lambda s: s.find(' ') == -1)})
def create_list(args):
    created = db.create_list(args['name'])
    response = Response()
    response.status_code = 201 if created else 409
    return response


@app.route('/lists/<name>/entries')
def entries_for_list(name):
    entries = db.list_entries(name)
    response = jsonify(entries)
    response.status_code = 200 if len(entries) > 0 else 404
    return response


@app.route('/lists/<list_name>/entries', methods=['POST'])
@use_kwargs({'text': Arg(str, required=True)})
def create_list_entry(list_name, text):
    created = db.create_entry(list_name, text)
    response = Response()
    response.status_code = 201 if created else 409
    return response


def convert_to_bool(arg):
    return arg.lower() in ('1', 'true')


@app.route('/lists/<name>/entries/<entry_id>', methods=['PATCH'])
def update_list_entry(name, entry_id):
    data = {k: v for k, v in
            parser.parse({'text': Arg(str),
                          'completed': Arg(bool, use=convert_to_bool)},
                         request, locations=('form',)).iteritems() if v}
    updated = db.update_entry(name, entry_id, data)
    response = Response()
    response.status_code = 200 if updated else 404
    return response


@app.route('/lists/<name>', methods=['DELETE'])
def delete_list(name):
    pass


if __name__ == '__main__':
    app.run(port=9080, debug=True)
