# -*- coding: utf-8 -*-

def index():
    return dict()

def getMaterias():
    materias = db().select(db.materia.ALL)
    return dict(materias = materias)

def getRegulares():
	regulares = db().select(db.estado_academico.ALL).first().regulares
	return dict(regulares = regulares)

def getAprobadas():
	aprobadas = db().select(db.estado_academico.ALL).first().aprobadas
	return dict(aprobadas = aprobadas)
