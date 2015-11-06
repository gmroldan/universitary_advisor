#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from json import dumps

class MateriaDTO:
	def __init__(self, materia_id, nombre, anio, esRegular, esAprobada):
		self.materia_id = materia_id
	        self.nombre = nombre
		self.anio = anio
	        self.esRegular = esRegular
	        self.esAprobada = esAprobada

	def setRegular(self, esRegular):
		self.esRegular = esRegular

	def setAprobada(self, esAprobada):
		self.esAprobada = esAprobada


	def getJSON(self):
		return dict(materiaid = self.materia_id, nombre = self.nombre, anio = self.anio, esRegular = self.esRegular, esAprobada = self.esAprobada)
