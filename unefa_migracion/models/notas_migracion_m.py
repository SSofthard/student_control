# -*- coding: utf-8 -*-
##############################################################################
#
#    Programa realizado por, Jeison Pernía y Jonathan Reyes en el marco
#    del plan de estudios de la Universidad Nacional Experimental
#    Politécnica de la Fuerza Armada, como TRABAJO ESPECIAL DE GRADO,
#    con el fin de optar al título de Ingeniero de Sistemas.
#    
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com
#
##############################################################################
from openerp.osv import fields, osv
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import * 
from openerp.tools.translate import _
from openerp import SUPERUSER_ID


class unefa_notas_migracion(osv.osv):
    _name='unefa.notas_migracion'
    _rec_name='estudiante_id'
    
    
    _columns={
        'pensum_id': fields.many2one('unefa.pensum', 'Pensum', required=True,
                                    help='Pensum de la asignatura.', 
                                    ),
        'periodo':fields.char('Período Académico',size=6,required=True, 
                                    help='Período en que fue cursada la asignatura'
                                    ),
        'asignatura_id': fields.many2one('unefa.asignatura','Asignatura', required=True,
                                    help='Asignatura académica.',
                                    ),
        'estudiante_id': fields.many2one('unefa.usuario_estudiante','Estudiante', 
                                    required=True,
                                    help='Estudiante.',
                                    ),
        'profesor_id': fields.many2one('unefa.usuario_profesor','Profesor', 
                                    required=True,
                                    help='Profesor.',
                                    ),
        'calificacion': fields.selection([
                        ('NP', 'NP'),
                        ('0', '0'),('1', '1'),('2', '2'),('3', '3'),
                        ('4', '4'),('5', '5'),('6', '6'),('7', '7'),
                        ('8', '8'),('9', '9'),('10', '10'),('11', '12'),
                        ('13', '13'),('14', '14'),('15', '15'),('16', '16'),
                        ('17', '17'),('18', '18'),('19', '19'),('20', '20'),
                        ],'Calificación',
                        required=True,
                        help='Calificación obtenida en la Asignatura. (NP - No Presentó)',
                        ),
        'active':fields.boolean('Activo',
                        help = """Si está activo el motor lo incluira en la vista."""),
        }
    
    
    _defaults = {
        'active':True,
        }
    
    _order = 'estudiante_id asc'
    
    def validar_notas(self, cr, uid, ids, estudiante_id, asignatura_id, context=None):
        notas_ids = self.search(cr,uid,[('estudiante_id','=',estudiante_id),
                                    ('asignatura_id','=',asignatura_id),
                                    ])
        data_notas = self.browse(cr,uid,notas_ids)
        for calificacion in data_notas:
            nota = int(calificacion.calificacion)
            if nota >= 10:
                raise osv.except_osv(
                    ('Alerta!'),
                    (u'Ya se encuentra registrada la asignatura %s, \
                     para el estudiante %s, con nota aprobada: %s puntos.'
                     %(calificacion.asignatura_id.asignatura,
                     calificacion.estudiante_id.nombre_completo,
                     calificacion.calificacion)))
        return True
    
    def create(self,cr,uid,vals,context=None):
        validar_asignatura = self.validar_notas(cr,uid,[],vals['estudiante_id'],vals['asignatura_id'])
        return super(unefa_notas_migracion,self).create(cr,uid,vals,context=context)
    
    
