# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

auth.settings.allow_basic_login = True
@auth.requires_login()
@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = [
            "/estado_academico[estado_academico]",
            "/estado_academico[estado_academico]/{estado_academico.usuario}",
            "/estado_academico[estado_academico]/{estado_academico.usuario}/:field"
            ]
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)

    def POST(table_name,**vars):
        print "Ingresando a post"
        if table_name in ('estado_academico', 'franja_horaria'):
            vars['usuario'] = auth.user.id
            print "usuario", auth.user.id
            return db[table_name].validate_and_insert(**vars)
        else:
            raise HTTP(400)

    def PUT(table_name, **vars):
        if table_name in ('estado_academico', 'franja_horaria'):
            record = db(db[table_name].usuario==auth.user.id).select().first()
            if record is None:
                return POST(table_name, **vars)
            vars['id'] = record.id
            print vars
            record.update(**vars)
            record.update_record()
            db.commit()
            return record.as_json()
        else:
            raise HTTP(400)

    return dict(GET=GET, POST=POST, PUT=PUT)
