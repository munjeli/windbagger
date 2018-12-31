from flask import Flask, render_template, request, redirect, url_for
import json
import gcp_util
import cfg

app = Flask(__name__)


@app.route('/')
def input_form():
    return render_template('address.html')


@app.route('/', methods=['POST'])
def post_input_form():
    address = request.form['address']
    gcp_util.fetch_reps_data()
    return redirect(url_for('local_data'))


@app.route('/federal')
def federal_data():
    return render_template('representative.html')


@app.route('/state')
def state_data():
    return render_template('representative.html')


@app.route('/local')
def local_data():
    entries = [r for r in cfg.rep_arr if r.level == 'local']
    return render_template('representative.html', level='Local', entries=entries)


if __name__ == '__main__':
    app.run()
