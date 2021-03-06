# -*- coding: utf-8 -*-
import logging
import pprint
import urllib

import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.payment_ogone.controllers.main import OgoneController

_logger = logging.getLogger(__name__)


class OgoneCompassion(OgoneController):
    @http.route([
        '/payment/ogone/accept', '/payment/ogone/test/accept',
        '/payment/ogone/decline', '/payment/ogone/test/decline',
        '/payment/ogone/exception', '/payment/ogone/test/exception',
        '/payment/ogone/cancel', '/payment/ogone/test/cancel',
    ], type='http', auth='none')
    def ogone_form_feedback(self, **post):
        """ Override to pass params to redirect url """
        transaction_obj = request.env['payment.transaction'].sudo()
        _logger.info('Ogone: entering form_feedback with post data %s',
                     pprint.pformat(post))  # debug
        transaction_obj.form_feedback(post, 'ogone')
        tx = transaction_obj._ogone_form_get_tx_from_data(post)
        tx.write({
            'postfinance_payid': post.get('PAYID'),
            'postfinance_brand': post.get('BRAND')
        })
        redirect = post.pop('return_url', '/') + '?' + urllib.urlencode(post)
        return werkzeug.utils.redirect(redirect)
