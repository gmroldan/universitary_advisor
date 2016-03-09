response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Inicio'),URL('default','index')==URL(),URL('default','index'),[]),
    (T('Estado Académico'),URL('estado_academico','index')==URL(),URL('estado_academico','index'),[]),
    (T('Disponibilidad Horaria'),URL('franja_horaria','index')==URL(),URL('franja_horaria','index'),[]),
    (T('Optimización'),URL('asistente','index')==URL(),URL('asistente','index'),[]),
]
