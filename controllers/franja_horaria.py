# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    record = db(db['franja_horaria'].usuario==auth.user.id).select().first()
    db.franja_horaria.usuario.readable = False
    db.franja_horaria.format = '%(hora_inicio)s'
    form = SQLFORM(db.franja_horaria, record, formstyle='table3cols',)
    form.element(_type='submit')['_class']='sofia'
    form.element(_type='submit')['_value']='Continuar'

    if form.process().accepted:
        redirect(URL('asistente','index'))
    elif form.errors:
        response.flash = 'Ocurrió un error al guardar.'
    return dict(form = form)
