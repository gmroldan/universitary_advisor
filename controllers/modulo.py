# -*- coding: utf-8 -*-
# intente algo como
def index():
    grid = SQLFORM.smartgrid(db.modulo, paginate=100)
    return dict(message="hello from modulo.py", grid=grid)


def carga_horaria():
    horarios = []
    modulos = db().select(db.modulo.ALL)

    for modulo in modulos:
        horarios.append(modulo.hora_inicio)

    return dict(horarios = sorted(horarios))


def resultado():
    return dict()
