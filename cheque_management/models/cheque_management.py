# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ChequeManagement(models.Model):
    _name = 'cheque.management'
    _description = "Cheque"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Name', required=True, readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one(comodel_name='res.partner', string="Vendor")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('pending_signature', 'Pending Signature'),
        ('signed', 'Signed'),
        ('submitted_to_client', 'Submitted to Client'),
        ('cancel', 'Cancelled'),
    ], 'Status', readonly=True, required=True, copy=False, tracking=True, default="draft")

    payment_type = fields.Selection([
        ('outbound', 'Send'),
        ('inbound', 'Receive'),
    ], string='Payment Type', default='inbound', required=True, tracking=True)

    amount = fields.Float(string='Amount', tracking=True)
    date = fields.Date(string='Date')
    memo = fields.Char(string='Memo')
    journal_id = fields.Many2one('account.journal', string='Journal')
    payment_id = fields.Many2one('account.payment', 'Payment')



    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('cheque.management') or _('New')
        return super(ChequeManagement, self).create(vals)

    def send_for_approval(self):
        self.state = 'pending_approval'

    def approve(self):
        self.state = 'pending_signature'

    def sign(self):
        self.state = 'signed'

    def submit_to_client(self):
        self.state = 'submitted_to_client'
        self.payment_id =  self.env['account.payment'].create({
            'name': self.name,
            'partner_id':self.partner_id.id,
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'journal_id': self.journal_id.id,
            'date': self.date,
            'ref': self.memo,
            'amount': self.amount,
        })
        self.payment_id.action_post()

    def button_payment(self):
        self.ensure_one()
        return {
            'name': _("Payment"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
            'view_mode': 'form',
            'res_id': self.payment_id.id,
        }

    def cancel(self):
        self.state = 'cancel'

    def reset_to_draft(self):
        self.state = 'draft'


class PaymentSignature(models.Model):

    _inherit = 'account.payment'

    signature = fields.Image(string='Signature')
    received_by = fields.Char(string='Received by')
    attachment = fields.Binary('Attachment', help=' You can attach the ID proof of the receiver or the copy of cheque. This will be visible in the payment receipt')

