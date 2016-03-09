#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import networkx as nx
from pulp import LpVariable, LpProblem, lpSum, LpBinary
from pulp import LpMaximize, LpStatus, value


class Asistente(object):
    def __init__(self, materias_plan, correlativas_plan, materias_regularizadas,
                    materias_aprobadas, franja_horaria_disponible, db=None):
        self.M = materias_plan
        self.C = correlativas_plan
        self.R = materias_regularizadas
        self.A = materias_aprobadas
        self.FH = franja_horaria_disponible
        self.__setup()

    def __setup(self):
        self.__generar_digrafo()
        self.__generar_subdigrafos()
        self.__determinar_MP()
        self.__determinar_coeficientes_de_beneficios()

    def __generar_digrafos(self):
        # Adjacency Relation for "Aprobadas para Cursar"
        APC = []
        # Digraph for for "Aprobadas para Cursar"
        DAPC = nx.DiGraph()
        # Adjacency Relation for "Regulares para Cursar"
        RPC = []
        # Digraph for "Regulares para Cursar"
        DRPC = nx.DiGraph()

        for materia in self.M:
            DAPC.add_node(materia.id)
            DRPC.add_node(materia.id)

        # List all pairs of the relations
        for c in self.C:
            APC.extend([[destination, source]
                for source, destination in zip([c.id] * len(c.rpc), c.apc)])
            RPC.extend([[destination, source]
                for source, destination in zip([c.id] * len(c.rpc), c.rpc)])

            # Add pairs as edges of the digraph DAPC.
            for pair in RPC:
                DAPC.add_edge(*pair)

            # Add pairs as edges of the digraph DRPC
            for pair in RPC:
                DRPC.add_edge(*pair)
        self.DAPC = DAPC
        self.DRPC = DRPC

    def __generar_subdigrafos(self):
        self.DAPCP = self.DAPC.copy()
        self.DRPCP = self.DRPC.copy()

        for materia in self.A:
                self.DAPCP.remove_node(materia)

        for materia in set(self.A + self.R):
                self.DRPCP.remove_node(materia)

    def __determinar_MP(self):
        self.MP = []
        for materia in self.DRPCP:
            if (self.DAPCP.in_degree(materia) +
                 self.DRPCP.in_degree(materia) == 0):
                self.MP.append(materia)

    def __determinar_coeficientes_de_beneficios(self):
        self.BI = self.DRPCP.out_degree()
        self.BLP = {}
        self.BLPF = {}
        self.BIF = {}
        self.BIT = {}

        for materia in self.BI.keys():
            beneficio_largo = 0
            beneficio_fraccion = 0
            beneficio_truncado = 0

            for correlativa in self.DRPCP[materia].keys():
                beneficio_fraccion += 1.0 / self.DRPCP.in_degree(correlativa)
                beneficio_truncado += int(1 / self.DRPCP.in_degree(correlativa))

                for correlativa2 in self.DRPCP[correlativa].keys():
                    beneficio_largo += 1.0 / self.DRPCP.in_degree(correlativa2)

            self.BLP[materia] = beneficio_largo
            self.BIF[materia] = beneficio_fraccion
            self.BLPF[materia] = self.BLP[materia] + self.BIF[materia]
            self.BIT[materia] = beneficio_truncado

    #def __generar_restricciones(self):
    #    horarios = db(db.horario_clases.materia.belongs(MP)).select()
