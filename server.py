from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime
from config import *

app = Flask(__name__)

# Paths to the JSON files
COUNTER_FILE = 'counters.json'
LOG_FILES = {
    'noa': 'noa_log.json',
    'milo': 'milo_log.json',
    'balder': 'balder_log.json',
    'lauge': 'lauge_log.json'
}
BUTTONS_FILE = 'static/buttons.json'

def read_counters():
    if not os.path.exists(COUNTER_FILE):
        return {'noa': 0, 'milo': 0, 'balder': 0, 'lauge': 0}
    with open(COUNTER_FILE, 'r') as f:
        return json.load(f)

def write_counters(counters):
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counters, f)

def read_log(name):
    if not os.path.exists(LOG_FILES[name]):
        return []
    with open(LOG_FILES[name], 'r') as f:
        return json.load(f)

def write_log(name, log):
    with open(LOG_FILES[name], 'w') as f:
        json.dump(log, f)

def read_buttons():
    if not os.path.exists(BUTTONS_FILE):
        return []
    with open(BUTTONS_FILE, 'r') as f:
        return json.load(f)

def read_template_buttons(name):
    file_path = f'static/{name}_buttons.json'
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/noa')
def noa():
    counters = read_counters()
    log = read_log('noa')
    buttons = read_buttons()
    template_buttons = read_template_buttons('noa')
    return render_template('index.html', counter=counters['noa'], log=log[-20:][::-1], buttons=buttons, template_buttons=template_buttons)

@app.route('/milo')
def milo():
    counters = read_counters()
    log = read_log('milo')
    buttons = read_buttons()
    template_buttons = read_template_buttons('milo')
    return render_template('milo.html', counter=counters['milo'], log=log[-20:][::-1], buttons=buttons, template_buttons=template_buttons)

@app.route('/balder')
def balder():
    counters = read_counters()
    log = read_log('balder')
    buttons = read_buttons()
    template_buttons = read_template_buttons('balder')
    return render_template('balder.html', counter=counters['balder'], log=log[-20:][::-1], buttons=buttons, template_buttons=template_buttons)

@app.route('/lauge')
def lauge():
    counters = read_counters()
    log = read_log('lauge')
    buttons = read_buttons()
    template_buttons = read_template_buttons('lauge')
    return render_template('lauge.html', counter=counters['lauge'], log=log[-20:][::-1], buttons=buttons, template_buttons=template_buttons)

@app.route('/noa/increment', methods=['POST'])
def increment_noa():
    return increment('noa')

@app.route('/milo/increment', methods=['POST'])
def increment_milo():
    return increment('milo')

@app.route('/balder/increment', methods=['POST'])
def increment_balder():
    return increment('balder')

@app.route('/lauge/increment', methods=['POST'])
def increment_lauge():
    return increment('lauge')

@app.route('/noa/decrement', methods=['POST'])
def decrement_noa():
    return decrement('noa')

@app.route('/milo/decrement', methods=['POST'])
def decrement_milo():
    return decrement('milo')

@app.route('/balder/decrement', methods=['POST'])
def decrement_balder():
    return decrement('balder')

@app.route('/lauge/decrement', methods=['POST'])
def decrement_lauge():
    return decrement('lauge')

@app.route('/noa/increment_by/<int:amount>', methods=['POST'])
def increment_noa_by(amount):
    counters = read_counters()
    counters['noa'] += amount
    button_label = request.form.get('button_label', '')

    log = read_log('noa')
    log_entry = {
        'date': datetime.now().strftime('%d-%m-%Y'),
        'change': f'+{amount}',
        'button_label': button_label
    }
    log.append(log_entry)
    write_log('noa', log)
    write_counters(counters)

    return redirect(url_for('noa'))

@app.route('/milo/increment_by/<int:amount>', methods=['POST'])
def increment_milo_by(amount):
    counters = read_counters()
    counters['milo'] += amount
    button_label = request.form.get('button_label', '')

    log = read_log('milo')
    log_entry = {
        'date': datetime.now().strftime('%d-%m-%Y'),
        'change': f'+{amount}',
        'button_label': button_label
    }
    log.append(log_entry)
    write_log('milo', log)
    write_counters(counters)

    return redirect(url_for('milo'))

@app.route('/balder/increment_by/<int:amount>', methods=['POST'])
def increment_balder_by(amount):
    counters = read_counters()
    counters['balder'] += amount
    button_label = request.form.get('button_label', '')

    log = read_log('balder')
    log_entry = {
        'date': datetime.now().strftime('%d-%m-%Y'),
        'change': f'+{amount}',
        'button_label': button_label
    }
    log.append(log_entry)
    write_log('balder', log)
    write_counters(counters)

    return redirect(url_for('balder'))

@app.route('/lauge/increment_by/<int:amount>', methods=['POST'])
def increment_lauge_by(amount):
    counters = read_counters()
    counters['lauge'] += amount
    button_label = request.form.get('button_label', '')

    log = read_log('lauge')
    log_entry = {
        'date': datetime.now().strftime('%d-%m-%Y'),
        'change': f'+{amount}',
        'button_label': button_label
    }
    log.append(log_entry)
    write_log('lauge', log)
    write_counters(counters)

    return redirect(url_for('lauge'))

def increment(name):
    counters = read_counters()
    if name not in counters:
        return "Page not found", 404
    try:
        amount = int(request.form.get('amount', 1))
    except ValueError:
        amount = 1
    reason = request.form.get('reason', '')
    counters[name] += amount

    log = read_log(name)
    log_entry = {
        'date': datetime.now().strftime('%d-%m-%Y'),
        'change': f'+{amount}',
        'reason': reason
    }
    log.append(log_entry)
    write_log(name, log)
    write_counters(counters)

    return redirect(url_for(f'{name}'))

def decrement(name):
    counters = read_counters()
    if name not in counters:
        return "Page not found", 404
    try:
        amount = int(request.form.get('amount', 1))
    except ValueError:
        amount = 1
    reason = request.form.get('reason', '')
    counters[name] -= amount

    log = read_log(name)
    log_entry = {
        'date': datetime.now().strftime('%d-%m-%Y'),
        'change': f'-{amount}',
        'reason': reason
    }
    log.append(log_entry)
    write_log(name, log)
    write_counters(counters)

    return redirect(url_for(f'{name}'))

if __name__ == '__main__':
    if debug:
        app.run(debug=True, port=port)
    elif debug == False:
        app.run(debug=False, host='0.0.0.0', port=port)