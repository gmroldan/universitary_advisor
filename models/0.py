from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'El Asistente'
settings.subtitle = 'ISI 2008 UTN FRT'
settings.author = 'Khouri, Lescano, Ibarra, Roldan'
settings.author_email = 'el.asistente.utn@gmail.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'mysql://root:root@localhost/elasistente'
settings.security_key = '8cae2d0f-78c7-4eb4-9f9c-75e942ac7676'
settings.email_server = 'smtp.gmail.com:587'
settings.email_sender = 'el.asistente.utn@gmail.com'
settings.email_login = 'el.asistente.utn@gmail.com:!Asistente1'
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
