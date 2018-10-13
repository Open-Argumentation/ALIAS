import json

from flask import Flask, render_template, jsonify
import os
import alias

app = Flask(__name__, template_folder='templates')
app.config['STATIC_FOLDER'] = 'static'
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

@app.route('/')
def demo():
    return render_template('index.html')

@app.route('/framework/<af_id>', methods=['POST'])
def framework(af_id):
    af = alias.read_tgf(static_file_dir + '/examples/' + af_id + '.tgf')
    return alias.get_json(af)


if __name__ == '__main__':
    app.run()

