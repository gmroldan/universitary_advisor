# -*- coding: utf-8 -*-
# intente algo como
def index():
    grid = SQLFORM.smartgrid(db.turno)
    return dict(message="hello from turno.py", grid = grid)
