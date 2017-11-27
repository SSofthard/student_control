$(document).ready(function () {
    var instance = openerp;
    openerp.web.data_export = {}; 
     $('a.exportar_csv').live('click',function(e) {
            if ((window.location.hash.search("#id=")) >= 0) {
                id = window.location.hash.split('&');
                id = id[0].split('#id=')[1];
                ids=parseInt(id);
                 openerp.session.get_file({ 
                    url: '/planilla_notas/exportar',
                    data: {ids},
                    complete: instance.web.unblockUI,
                     });
             }
         });
                
             
             
         });
        
        
