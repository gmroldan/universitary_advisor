# -*- coding: utf-8 -*-
from MateriaDTO import MateriaDTO

def index():
	estado_academico = db(db['estado_academico'].usuario==auth.user.id).select().first()
	
	if estado_academico is None:
		db['estado_academico'].validate_and_insert(usuario = auth.user.id, regulares = [], aprobadas = [])
	
	materias_dto = []
	materias = db().select(db.materia.ALL)
	regulares = db(db['estado_academico'].usuario==auth.user.id).select(db.estado_academico.ALL).first().regulares
	aprobadas = db(db['estado_academico'].usuario==auth.user.id).select(db.estado_academico.ALL).first().aprobadas

	for materia in materias:
		materia_dto = MateriaDTO(materia.id, materia.nombre, materia.anio, False, False)
		if materia.id in regulares:
			materia_dto.setRegular(True)

		if materia.id in aprobadas:
			materia_dto.setAprobada(True)

		materias_dto.append(materia_dto.getJSON())
	return dict(materias_dto = materias_dto)

def submit():
	import gluon.contrib.simplejson
	materias_dto = gluon.contrib.simplejson.loads(request.body.read())

	estado_academico = db(db['estado_academico'].usuario==auth.user.id).select().first()
	estado_academico.regulares = []	
	estado_academico.aprobadas = []

	for materia_dto in materias_dto:		
		if materia_dto['esRegular']:
			estado_academico.regulares.append(materia_dto['materiaid'])
	
		if materia_dto['esAprobada']:
			estado_academico.aprobadas.append(materia_dto['materiaid'])

	estado_academico.update_record()
	db.commit()

	return dict(estado_academico = estado_academico)
