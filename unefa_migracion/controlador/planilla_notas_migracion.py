# -*- coding: utf-8 -*-
import base64
import werkzeug
import werkzeug.urls
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request, STATIC_CACHE
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
from datetime import datetime,date
import time 
import logging

logger = logging.getLogger(__name__)



class planilla_notas_migracion(http.Controller):
    
    
    @http.route('/planilla_notas/exportar', type='http', auth='public', website=True)
    def exportar_lista(self, **values):
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        planilla_notas_obj = registry['unefa.planilla_notas']
        planilla_notas_id = planilla_notas_obj.crear_planilla_notas(cr,SUPERUSER_ID, int(values['ids'].encode('utf-8')), values['token'])
        return planilla_notas_id
           
        
   
