import json
import requests
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Markup


client_code = '4807395013948353036'
client_secret = '5d620491b5d91462cc2c945db562bc40a1c02c57840a554c7e1cde025ded513f'

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='2\x8f\xc3+\x8b\xf2H[\x1a\xcd\xa0\xdd\xb0<s\xcc\x10\x94\x05\xf5\xf1\xd0\xbf['
))


@app.route('/')
def site_root():
    return Markup('This is stormgiant.net'+ session['access_token'])


@app.route('/pinterest/login')
def pinterest_login():
    url = 'https://api.pinterest.com/oauth/'
    url += '?response_type=code'
    url += '&client_id=' + client_code
    url += '&state=tw399afd'
    url += '&redirect_uri=https://stormgiant.net/pinterest/connect'
    url += '&scope=read_public,write_public'
    return redirect(url,code=302) 


@app.route('/pinterest/connect')
def pinterest_connect():
    url = 'https://api.pinterest.com/v1/oauth/token'
    payload = {'grant_type': 'authorization_code', 
               'client_id': client_code,
               'client_secret': client_secret,
               'code': request.args.get('code','')}
    r = requests.post(url,payload)
    session['access_token'] = r.json()['access_token']
    return redirect('https://stormgiant.net/pinterest', code=302)


@app.route('/pinterest')
def pinterest_home():
    if session['access_token'] is not None:
        boards = get_boards()
        return render_template('pinterest.html', boards=boards)
    else:
        return render_template('pinterest.html')


def get_boards():
    payload = { 'access_token':session['access_token'], 'fields':'id,name'}
    r = requests.get('https://api.pinterest.com/v1/me/boards/', params=payload)
    return r.json()

def get_pins_for_board():
    payload = { 'access_token':session['access_token'], 'fields':'id,name'}
    r = requests.get('https://api.pinterest.com/v1/me/boards/', params=payload)
    return r.json()