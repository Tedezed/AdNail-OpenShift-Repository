#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import os
from os import path
from bottle import *
from ANResult import AdNailResultado

appid = 'micasaa3b-ad29-4b11-ac66-115e152e910'

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

@get('/css/<filename:re:.*>')
def sever_static(filename):
    if ON_OPENSHIFT:
        return static_file(filename, root=os.environ['OPENSHIFT_REPO_DIR']+'/wsgi/static/css')
    else:
        return static_file(filename, root='static/css')

@get('/img/<filename:re:.*>')
def sever_static(filename):
    if ON_OPENSHIFT:
        return static_file(filename, root=os.environ['OPENSHIFT_REPO_DIR']+'/wsgi/static/img')
    else:
        return static_file(filename, root='static/img')

@get('/js/<filename:re:.*>')
def sever_static(filename):
    if ON_OPENSHIFT:
        return static_file(filename, root=os.environ['OPENSHIFT_REPO_DIR']+'/wsgi/static/js')
    else:
        return static_file(filename, root='static/js')

@get('/font/<filename:re:.*>')
def sever_static(filename):
    if ON_OPENSHIFT:
        return static_file(filename, root=os.environ['OPENSHIFT_REPO_DIR']+'/wsgi/static/font')
    else:
        return static_file(filename, root='static/font')

@route('/')
def index():
    return template('index.html')

@get('/busqueda')
def entrada():
    return template('busqueda.html')

@get('/contacto')
def contacto():
    return template('contacto.html')

@post('/resultado')
def resultado():
    entrada = ''
    numpag = 1
    response.set_cookie('busqueda', str(numpag))
    resultadnail = AdNailResultado(appid,numpag,entrada)
    return resultadnail

@route('/resultado+')
def resultado():
    entrada = request.cookies.get('entrada', 'entrada')
    numpag = int(request.cookies.get('busqueda', 'metodo'))
    if numpag < 35:
        numpag = numpag + 1
    response.set_cookie('busqueda', str(numpag))

    try:
        return AdNailResultado(appid,numpag,entrada)
    except:
        return template('busqueda_error.html')

@route('/resultado-')
def resultado():
    entrada = request.cookies.get('entrada', 'entrada')
    numpag = int(request.cookies.get('busqueda', 'metodo'))
    if numpag > 1:
        numpag = numpag - 1
    response.set_cookie('busqueda', str(numpag))

    try:
        return AdNailResultado(appid,numpag,entrada)
    except:
        return template('busqueda_error.html')

if ON_OPENSHIFT:
    TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/'))
    application=default_app()
else:
    print "AdNail - Interfaces disponibles: "
    print commands.getoutput("/sbin/ifconfig | egrep -o '^[a-z].......'")
    intfz = raw_input('Introduce la interfaz a utilizar: ')
    comand = "/sbin/ifconfig "+intfz+" | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | egrep -v '*(0|255)$'"
    iphost = commands.getoutput(comand)
    print "La IP del Servidor es: ", iphost
    run(host=iphost, port=8080, debug=True)
