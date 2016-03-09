#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
from pulp import LpVariable, LpProblem, lpSum, LpBinary
from pulp import LpMaximize, LpStatus, value
#local_import('module', reload=True)
import time
class Asistente(object):
    def __init__(self, materias_plan, correlativas_plan, materias_regularizadas,
                    materias_aprobadas, franja_horaria_disponible, db=None):
        self.M = materias_plan
        self.C = correlativas_plan
        self.R = materias_regularizadas
        self.A = materias_aprobadas
        self.FH = ['O' + str(o) for o in franja_horaria_disponible]
        print "FH", self.FH
        self.__setup()

    def __setup(self):
        self.inicio = time.time()
        print "########################Inicio:"
        self.__generar_digrafos()
        self.__generar_subdigrafos()
        self.__determinar_MP()
        self.__determinar_coeficientes_de_beneficios()
        self.__determinar_carga_horaria()
        self.__preparar_restricciones()
        self.__generar_restricciones()
        self.__optimizar_cursado()
        self.__generar_imagenes()
        self.__analisis_optimo()
        self.cursado.writeLP("cursado.lp")

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
            for pair in APC:
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

    def __generar_imagenes(self):
        A = nx.to_agraph(self.DRPC)        # convert to a graphviz graph
        A.layout(prog='dot')            # neato layout
        A.draw("DRPC.png", prog='dot')

        A = nx.to_agraph(self.DAPC)        # convert to a graphviz graph
        A.layout()
        A.draw("DAPC.png", prog='dot')

        A = nx.to_agraph(self.DRPCP)        # convert to a graphviz graph
        A.layout(prog='dot')            # neato layout
        A.draw("DRPCP.png", prog='dot')

        A = nx.to_agraph(self.DAPCP)        # convert to a graphviz graph
        A.layout()
        A.draw("DAPCP.png", prog='dot')
    def __determinar_MP(self):
        self.MP = []
        for materia in self.DRPCP:
            if (self.DAPCP.in_degree(materia) +
                 self.DRPCP.in_degree(materia) == 0):
                try:
                    h = db(db.materia.id==materia).select().first()
                    h = int(h.segundo_cuatrimestre)
                except:
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

    def __determinar_carga_horaria(self):
        def str2intor0(x):
            try:
                return int(x)
            except:
                return 0
        self.carga_horaria = {}
        for row in self.M:
            self.carga_horaria[row.id] = str2intor0(row.anual) +\
                          str2intor0(row.primer_cuatrimestre) +\
                             str2intor0(row.segundo_cuatrimestre)
#################
    def __preparar_restricciones(self):
        horarios = db(db.horario_clases.materia.belongs(self.MP)).select()
        self.variables = []
        self.materias = []
        self.materias_id = []
        self.nombre_materias = {}
        self.materia_comision = []
        carga = self.carga_horaria
        self.r1 = {}
        self.r2 = {}
        self.r3 = {}
        self.r4 = {}
        self.r5 = []
        for horario in horarios:
            try:
                turno = str(horario.turno)
                materia = str(horario.materia)
                #nombre = str(horario.materia.nombre)
                comision = str(horario.comision)
                dia = str(horario.dia)
                modulos = horario.modulo
                #print modulos
            except IndexError:
                continue

            #Determinar Horas de Cursado
            materia = 'M' + materia
            turno = 'T' + turno
            comision = 'C' + comision
            dia = 'D' + dia
            materia_id = horario.materia.id
            materia_nombre = horario.materia.nombre

            for o in modulos:
                #print materia, comision, o
                o = 'O' + str(o)
                self.variables.append(materia + comision + dia + o)

                if materia not in self.materias:
                    self.variables.append(materia)
                    self.materias.append(materia)
                    self.materias_id.append(materia_id)
                    self.nombre_materias[materia] = materia_nombre
                if materia + comision not in self.materia_comision:
                    self.variables.append(materia + comision)
                    self.materia_comision.append(materia + comision)
                    # dia modulo
                if not self.r1.has_key(dia + o):
                    self.r1[dia + o] = []
                self.r1[dia + o] += [(materia, comision, dia, o)]

                # cursado completo
                if not self.r2.has_key(materia + comision):
                    self.r2[materia + comision] = []
                self.r2[materia + comision] += [(str(carga[materia_id]), materia, comision, dia, o)]

                # 1 sola comision
                if not self.r3.has_key(materia):
                    self.r3[materia] = []
                self.r3[materia] += [(str(carga[materia_id]), materia, comision, dia, o)]
                # TODO colisiones
                # no superposicion entre turnos
                
                colisiones = [('13', '15'),('14', '15'),('14', '16')]
                for colision in colisiones:
                    if turno + o in colision:
                        key = ".".join(colision)
                        key = dia + key
                        if not r4.has_key(key):
                            r4[key] = []
                        r4[key] += [(materia, comision, dia, o)]
                
                # franja horaria
                if o not in self.FH:
                    print o
                    self.r5.append((materia,comision, dia, o))

    def __generar_restricciones(self):
        X = LpVariable.dicts('X', self.variables, cat = LpBinary)
        self.cursado = LpProblem("Cursado",LpMaximize)

        # "\n\n Restricciones de dia-modulo\n\n"
        i = 1
        for r in self.r1.values():
            self.cursado += lpSum([X["".join(x)] for x in r]) <= 1, \
            "_1C" + str(i).zfill(3)
            i += 1

        #"\n\n Restricciones de cursado completo\n\n"

        for r in self.r2.values():
            self.cursado += int(r[0][0]) *X[r[0][1]+r[0][2]] == lpSum([X["".join(x[1:])] for x in r]), \
            "_2C" + str(i).zfill(3)
            i += 1
        #"""

        #"\n\n Restricciones 1 sola comision\n\n"
        for r in self.r3.values():
            self.cursado += int(r[0][0]) *X[r[0][1]] == lpSum([X["".join(x[1:])] for x in r]), \
            "_3C" + str(i).zfill(3)
            i += 1

        #"\n\n Restricciones de Colision\n\n"
        for r in self.r4.values():
            self.cursado += lpSum([X["".join(x)] for x in r]) <= 1, \
            "_4C" + str(i).zfill(3)
            i += 1

        #"\n\n Restricciones de franja horaria\n\n"

        for r in [x + "" for x in ["".join(x) for x in self.r5]]:
            self.cursado += X[r] == 0, \
            "_5C" + str(i).zfill(3)
            i += 1

        self.X = X

    def __optimizar_cursado(self):
        self.cursado += lpSum([1 + 5 * self.BIF[m] +
                       self.BLP[m] +
                       self.BIT[m] +
                       self.BI[m] *
                      self.X['M'+str(m)] for m in self.materias_id])
        self.status = self.cursado.solve()
        while(self.status != 1):
            print "Optimizando..."
            time.sleep(0.5)

    def __analisis_optimo(self):
        def result():
            resultados = {}
            for x in self.X.keys():
                resultados[x] = value(self.X[x])
            return resultados

        def materias_decididas():
            decididas = []
            for x in self.materias:
                if round(value(self.X[x])) > 0.0:
                    decididas.append(x)
            return decididas

        def cantidad_materias():
            return len(materias_decididas())

        def horarios():
            tabla_horarios = {}
            for x in self.X.keys():
                try:
                    if float(value(self.X[x])) > 0.0:
                        if len(x) > 5:
                            mc = x.split("D")[0]
                            tdm = x.split("D")[1]
                            materia_comision = mc.split('C')
                            materia_comision[0] = self.nombre_materias[materia_comision[0]]
                            tabla_horarios["D"+tdm] = materia_comision
                        else:
                            continue
                except ValueError:
                    continue
            return tabla_horarios

        self.tabla_horarios = horarios()


@auth.requires_login()
def index():
    usuario_id = auth.user.id
    estado_academico = db(db.estado_academico.usuario == usuario_id).select().first()
    M = db().select(db.materia.ALL)
    C = db().select(db.correlativa.ALL)
    A = estado_academico.aprobadas
    R = estado_academico.regulares
    FH = db(db.franja_horaria.usuario == usuario_id).select().first().modulos

    asistente = Asistente(materias_plan=M, correlativas_plan=C, materias_regularizadas=R,
                    materias_aprobadas=A, franja_horaria_disponible=FH)
    MP = db(db.materia.id.belongs(asistente.MP)).select(orderby=db.materia.nombre)
    if len(MP) == 1:
        elegibles = MP[0]
    elif len(MP) >= 2:
        elegibles = ", ".join([m.nombre for m in MP[:-1]])
        elegibles += " y " + MP[-1].nombre + "."
    else:
        elegibles = "No hay materias elegibles."
    return dict(FH=FH, MP=MP, estado=asistente.status, horarios = asistente.tabla_horarios, elegibles=elegibles)
