# -*- coding: utf-8 -*-
@auth.requires_login()
def estado_academico():
    record = db(db['estado_academico'].usuario==auth.user.id).select().first()
    db.estado_academico.regulares.requires = IS_IN_DB(db, 'materia.id','%(anio)s - %(nombre)s', 
                                                      multiple = True, orderby = 'materia.anio' )
    db.estado_academico.aprobadas.requires = IS_IN_DB(db, 'materia.id','%(anio)s - %(nombre)s', 
                                                      multiple = True, orderby = 'materia.anio' )
    db.estado_academico.usuario.readable = False
    form = SQLFORM(db.estado_academico, record)

    if form.process().accepted:
        session.flash = 'Estado académico actualizado.'
        redirect(URL('franja_horaria'))
    elif form.errors:
        response.flash = 'Ocurrió un error al guardar.'
    else:
        response.flash = 'Completá tu estado académico.'
        
    return dict(form = form)

@auth.requires_login()
def franja_horaria():
    record = db(db['franja_horaria'].usuario==auth.user.id).select().first()
    db.franja_horaria.usuario.readable = False
    db.franja_horaria.format = '%(hora_inicio)s'
    form = SQLFORM(db.franja_horaria, record)

    if form.process().accepted:
        session.flash = 'Franja Horaria Actualizada.'
        redirect(URL('optimizar'))
    elif form.errors:
        response.flash = 'Ocurrió un error al guardar.'
    else:
        response.flash = 'Elegí tu franja horaria.'
        
    return dict(form = form)

def optimizar():
    redirect(URL('asistente', 'index'))
    return dict()
