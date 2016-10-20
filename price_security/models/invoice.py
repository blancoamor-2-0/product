# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    product_can_modify_prices = fields.Boolean(
        related='product_id.can_modify_prices',
        readonly=True,
        string='Product Can modify prices')

    @api.multi
    @api.constrains(
        'discount', 'product_can_modify_prices')
    def check_discount(self):
        for invoice_line in self:
            if (invoice_line.user_has_groups(
                    'price_security.group_restrict_prices'
            ) and not invoice_line.product_can_modify_prices and invoice_line.
                invoice_id
            ):
                invoice_line.env.user.check_discount(
                    invoice_line.discount,
                    invoice_line.invoice_id.partner_id.
                    property_product_pricelist.id)
