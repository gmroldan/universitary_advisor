# -*- coding: utf-8 -*-
# intente algo como
def index():
    grid = SQLFORM.smartgrid(db.modulo, paginate=100)
    return dict(message="hello from modulo.py", grid=grid)
