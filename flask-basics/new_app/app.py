import json

from flask import (Flask, render_template, redirect,
                   url_for, request, make_response, flash)

from options import DEFAULTS

app = Flask(__name__)
app.secret_key = 'sfjkui3n323i2229239IUDHFdkf*($U$#UJ)'


@app.route('/')
def index():
    return render_template('index.html', saves=get_saved_data())


@app.route('/save', methods=['POST'])
def save():
    # import pdb; pdb.set_trace() # debug nesto kao breakpoint
    flash("Saved changes")
    response = make_response(redirect(url_for('builder')))
    data = get_saved_data()
    data.update(dict(request.form.items()))
    response.set_cookie('cookie', json.dumps(dict(data)))
    return response


@app.route('/builder')
def builder():
    return render_template(
        'builder.html',
        saves=get_saved_data(),
        options=DEFAULTS
    )


def get_saved_data():
    try:
        data = json.loads(request.cookies.get('cookie'))
    except TypeError:
        data = {}
    return data


app.run(debug=True, host='0.0.0.0', port=8000)
