#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, post, route, request, run, template, static_file, response
from shift_local import shift_local
from ANResult import AdNailResultado

appid = 'micasaa3b-ad29-4b11-ac66-115e152e910'

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
        return template('busqueda_error.html')

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

#Deteccion de entorno, OpenShift o local.
shift_local()
