import json

from flask import Flask, render_template, jsonify, request
import os
import alias

app = Flask(__name__, template_folder='templates')
app.config['STATIC_FOLDER'] = 'static'
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

af = None;

@app.route('/')
def demo():
    return render_template('index.html')

@app.route('/framework/<af_id>', methods=['POST'])
def framework(af_id):
    global af
    af = alias.read_tgf(static_file_dir + '/examples/' + af_id + '.tgf')
    return alias.get_json(af)

@app.route('/extension/<ext_id>', methods=['POST'])
def extension(ext_id):
    global af
    if af is not None:
        if ext_id == 'Stable':
            return json.dumps([list(v) for v in af.get_stable_extension()])
        if ext_id == 'Complete':
            return json.dumps([list(v) for v in af.get_complete_extension()])
        if ext_id == 'Preferred':
            return json.dumps([list(v) for v in af.get_preferred_extension()])
    else:
        return "Please select argumentation framework first"


@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        global af
        file.save(os.path.join("./", file.filename))
        af = alias.read_tgf("./" + file.filename)
        return alias.get_json(af)

if __name__ == '__main__':
    app.run()

