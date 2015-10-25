# -*- coding: utf-8 -*-

def index():
    anios = {'1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five'}
    materias = db().select(db.materia.ALL)
    estado_academico = db().select(db.estado_academico.ALL)
    ##grid = SQLFORM.grid(db.estado_academico, maxtextlength=150)
    return dict(anios = anios, materias = materias, estado_academico = estado_academico)
