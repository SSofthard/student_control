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
import werkzeug.urls
from openerp.addons.web.controllers.main import login_redirect
from openerp.http import request, STATIC_CACHE
from openerp.addons.web.controllers import main
from openerp import http
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('UTF8')



class unefa_planilla_notas(osv.osv):
    _name='unefa.planilla_notas'
    _rec_name='asignatura_id'
    
    _columns={
        'pensum_id': fields.many2one('unefa.pensum', 'Pensum', required=True,help='Pensum de la asignatura.', ),
        'asignatura_id': fields.many2one('unefa.asignatura','Asignatura', required=True,help='Asignatura académica.',),
        'active':fields.boolean('Activo',help = """Si está activo el motor lo incluira en la vista."""),
        
        }
    
    _defaults = {
        'active':True,
        }
    
    def domain_asignatura(self,cr,uid,ids,pensum_id,context=None):
        if pensum_id:
            list_asignatura = []
            dominio = {}
            pensum_obj = self.pool.get('unefa.pensum')
            pensum_data = pensum_obj.browse(cr,uid,int(pensum_id))
            for semestre in pensum_data.semestre_ids:
                for asignatura in semestre.asignaturas_ids:
                    list_asignatura.append(int(asignatura))
            dominio={'asignatura_id': [('id', 'in', list_asignatura)]}
            return {'domain':dominio}
            
            
    def limpiar_campos(self,cr,uid,ids,campo,context=None):
        return {'value':{campo:''}}
    
    
    def crear_planilla_notas(self,cr,uid, ids, token, context=None):
        lista=[]
        list_rows=[]
        header=['Pensum',
                'AsignaturaGuia',
                'Asignatura/Id. de la BD',
                'EstudianteGuia',
                'Estudiante/Id. de la BD',
                'CédulaGuia',
                'Calificación',
                'Período Académico',
                'profesor_id/Id. de la BD'
                ]
        users_obj = self.pool.get('res.users')
        semestre_obj = self.pool.get('unefa.semestre')
        
        
        users_estudiante_obj = self.pool.get('unefa.usuario_estudiante')
        for records in self.browse(cr,uid,ids):
            semestre_id = semestre_obj.search(cr,uid,[('asignaturas_ids','=',records.asignatura_id.id)])
            users_estudiante_ids=users_estudiante_obj.search(cr,uid,[('pensum_id','=',records.pensum_id.id),('semestre_id','>=',semestre_id[0])])
            data_users_estudiante=users_estudiante_obj.browse(cr,uid,users_estudiante_ids)
            for estudiante in data_users_estudiante:
                lista.append(records.pensum_id.pensum)
                lista.append(records.asignatura_id.asignatura)
                lista.append(records.asignatura_id.id)
                lista.append(estudiante.nombre_completo)
                lista.append(estudiante.id)
                lista.append(estudiante.user_id.cedula)
                
                list_rows.append(lista)
                lista=[]
        export_obj=main.CSVExport()
        return http.HttpRequest(request.httprequest).make_response(export_obj.from_data(header, list_rows),
            headers=[('Content-Disposition',
                            main.content_disposition(export_obj.filename(records.asignatura_id.asignatura))),
                     ('Content-Type', export_obj.content_type)],
                    )
            
