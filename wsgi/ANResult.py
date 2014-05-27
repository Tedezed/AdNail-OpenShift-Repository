#!/usr/bin/env python
# -*- coding: utf-8 -*-
def AdNailResultado(appid,numpag,entrada):
	from bottle import template
	from ebay import *
	from BrainSlug import *
	try:
		dicebay = busqueda(appid,numpag,entrada)
	except:
		dicebay = ''
	dicma = BrainSlugMA(numpag,entrada)
	dicta = BrainSlugTA(numpag,entrada)

	if dicebay or dicma or dicta:
		listtitulo = []
		listlink = []
		listprecio = []
		listphoto =  []
		listmoneda = []
		listmetodo = []

		if not dicta == '':
			cont_ta = 0
			for i in dicta['listtitulo_ta']:
				cont_ta += 1
			cont_ta = cont_ta -1

		if not dicma == '':
			cont_ma = 0
			for i in dicma['listtitulo_ma']:
				cont_ma += 1
			cont_ma = cont_ma -1

		if not dicebay == '':
			cont_ebay = 0
			for i in dicebay['listtitulo_ebay']:
				cont_ebay += 1
			cont_ebay = cont_ebay

		llave = 0
		while llave < 19:
			if not dicebay == '' and llave < cont_ebay:
				listtitulo.append(dicebay['listtitulo_ebay'][llave])
				listlink.append(dicebay['listlink_ebay'][llave])
				listprecio.append(dicebay['listprecio_ebay'][llave])
				listphoto.append(dicebay['listphoto_ebay'][llave])
				listmoneda.append(dicebay['listmoneda_ebay'][llave])
				listmetodo.append(dicebay['listmetodo_ebay'][llave])

			if not dicma == '' and llave < cont_ma:
				listtitulo.append(dicma['listtitulo_ma'][llave])
				listlink.append(dicma['listlink_ma'][llave])
				listprecio.append(dicma['listprecio_ma'][llave])
				listphoto.append(dicma['listphoto_ma'][llave])
				listmoneda.append(dicma['listmoneda_ma'][llave])
				listmetodo.append(dicma['listmetodo_ma'][llave])

			if not dicta == '' and llave < cont_ta:
				listtitulo.append(dicta['listtitulo_ta'][llave])
				listlink.append(dicta['listlink_ta'][llave])
				listprecio.append(dicta['listprecio_ta'][llave])
				listphoto.append(dicta['listphoto_ta'][llave])
				listmoneda.append(dicta['listmoneda_ta'][llave])
				listmetodo.append(dicta['listmetodo_ta'][llave])

			llave += 1

		return template('resultado.html',listtituloh=listtitulo,listlinkh=listlink,listprecioh=listprecio,
			listphotoh=listphoto,listmonedah=listmoneda,listmetodoh=listmetodo, numpagh=numpag)
	else:
		return template('busqueda_error.html',entradah=entrada)