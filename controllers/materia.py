# -*- coding: utf-8 -*-
# intente algo como
def index():
    grid = SQLFORM.smartgrid(db.materia, maxtextlength=150, paginate=100)
    return dict(message="hello from materia.py", grid=grid)
