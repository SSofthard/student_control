# -*- coding: utf-8 -*-

from openerp.addons.web import http
from openerp.addons.web.controllers.main import Database, db_list
openerpweb = http

class Database_restrict(Database):
    @openerpweb.jsonrequest
    def create(self, req, fields):
        
        # check if it is not first installation - restrict!
        
        dblist = db_list(req)
        if len(dblist) > 0:
            raise Exception('Not allowed')

        return super(Database_restrict, self).create(req, fields)

    @openerpweb.jsonrequest
    def duplicate(self, req, fields):
        raise Exception('Not allowed')

    @openerpweb.jsonrequest
    def drop(self, req, fields):
        raise Exception('Not allowed')

    @openerpweb.httprequest
    def backup(self, req, backup_db, backup_pwd, token):
        raise Exception('Not allowed')

    @openerpweb.httprequest
    def restore(self, req, db_file, restore_pwd, new_db):
        raise Exception('Not allowed')

    @openerpweb.jsonrequest
    def change_password(self, req, fields):
        raise Exception('Not allowed')
    
    _cp_path = ''


    def manager(self, **kw):
        return http.local_redirect('/')
        #~ raise Exception('Not allowed')
    
    @http.route('/web/database/selector', type='http', auth="none")
    def selector(self, **kw):
        return http.local_redirect('/')
        #~ raise Exception('Not allowed')
        
        
        
        
