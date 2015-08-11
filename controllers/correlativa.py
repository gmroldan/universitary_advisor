# -*- coding: utf-8 -*-
# intente algo como
def index():
    grid = SQLFORM.smartgrid(db.correlativa, maxtextlength=150, paginate=100)
    return dict(message="hello from correlativa.py", grid = grid)
