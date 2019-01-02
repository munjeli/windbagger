from flask import Flask, render_template, request, redirect, url_for
import logging
import gcp_util
import cfg

fmt = "%(levelname)s\t%(funcName)s():%(lineno)i\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/')
def input_form():
    cfg.rep_arr = []
    return render_template('address.html')


@app.route('/', methods=['POST'])
def post_input_form():
    address = request.form['address']
    response = gcp_util.fetch_reps_data(address)
    if response == 'address not found':
        return redirect(url_for('input_form'))
    else:
        return redirect(url_for('local_data'))


@app.route('/federal')
def federal_data():
    entries = [r for r in cfg.rep_arr if r.level == 'federal']
    return render_template('representative.html', level='Federal', entries=entries)


@app.route('/state')
def state_data():
    entries = [r for r in cfg.rep_arr if r.level == 'state']
    return render_template('representative.html', level='State', entries=entries)


@app.route('/local')
def local_data():
    entries = [r for r in cfg.rep_arr if r.level == 'local']
    return render_template('representative.html', level='Local', entries=entries)


@app.route('/about')
def about_data():
    return render_template('about.html')


@app.route('/campaigns')
def campaign_data():
    return render_template('campaigns.html')


@app.route('/oped')
def op_ed():
    return render_template('oped.html')


if __name__ == '__main__':
    app.run()
