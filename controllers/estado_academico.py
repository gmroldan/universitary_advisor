# -*- coding: utf-8 -*-
from MateriaDTO import MateriaDTO

def index():
	materias_dto = []
	materias = db().select(db.materia.ALL)
	regulares = db().select(db.estado_academico.ALL).first().regulares
	aprobadas = db().select(db.estado_academico.ALL).first().aprobadas

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
	data = gluon.contrib.simplejson.loads(request.body.read())
	# Guardar datos en DB.
	return dict(data = data)
