# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: David Coninckx <david@coninckx.com>
#
#    The licence is in the file __manifest__.py
#
##############################################################################
from odoo import models, fields, api


class CompassionChild(models.Model):
    _inherit = 'compassion.child'

    desc_fr = fields.Text('French description', readonly=True)
    desc_de = fields.Text('German description', readonly=True)
    desc_it = fields.Text('Italian description', readonly=True)

    @api.model
    def correct_old_children(self):
        old_children = self.search([('global_id', '=', False)]).filtered(
            lambda c: len(c.local_id) < 11)
        for child in old_children:
            if child.code:
                child.local_id = child.code[0:2] + '0' + \
                    child.code[2:5] + '0' + child.code[5:]
        return True

    @api.model
    def find_missing_global_id(self):
        missing_gids = self.search([('global_id', '=', False)])
        global_search = self.env['compassion.childpool.search'].create({
            'take': 1,
        })
        cpt = 0
        for child in missing_gids:
            try:
                global_search.local_id = child.local_id
                global_search.do_search()
                if global_search.global_child_ids:
                    child.global_id = global_search.global_child_ids.global_id
                # Commit at each fix
                self.env.cr.commit()    # pylint: disable=invalid-commit
            except:
                self.env.invalidate_all()
            finally:
                cpt += 1
