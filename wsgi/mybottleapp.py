#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, post, route, request, run, template, static_file, response, default_app
from shift_local import shift_local
from ANResult import AdNailResultado

fil = open('Key.conf','r')
key = ''
for lin in fil:
    key = key + lin
key = key.replace("\n","")
fil.close()
exec key

@get('/css/<filename:re:.*>')
def sever_static(filename):
    return static_file(filename, root='css')

@get('/img/<filename:re:.*>')
def sever_static(filename):
    return static_file(filename, root='img')

@get('/js/<filename:re:.*>')
def sever_static(filename):
    return static_file(filename, root='js')

@get('/font/<filename:re:.*>')
def sever_static(filename):
    return static_file(filename, root='font')

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
    try:
        return AdNailResultado(appid,numpag,entrada)
    except:
        return template('index.html')

@route('/resultado+')
def resultado():
    entrada = request.cookies.get('entrada', 'entrada')
    numpag = int(request.cookies.get('busqueda', 'metodo'))
    if numpag < 90:
        numpag = numpag + 1
    response.set_cookie('busqueda', str(numpag))

    try:
        return AdNailResultado(appid,numpag,entrada)
    except:
        return template('index.html')

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
        return template('index.html')

#Deteccion de entorno, OpenShift o local.
import os
from bottle import TEMPLATE_PATH

ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True

if ON_OPENSHIFT:
    TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'],'runtime/repo/wsgi/views/'))

    application=default_app()
else:
    import commands
    from bottle import run

    print "AdNail - Interfaces disponibles: "
    print commands.getoutput("/sbin/ifconfig | egrep -o '^[a-z].......'")
    intfz = raw_input('Introduce la interfaz a utilizar: ')
    comand = "/sbin/ifconfig "+intfz+" | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | egrep -v '*(0|255)$'"
    iphost = commands.getoutput(comand)
    print "La IP del Servidor es: ", iphost
    run(host=iphost, port=8080, debug=True)