from odoo import api, fields, models
from odoo import http, tools, _
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.auth_signup.models.res_users import SignupError

SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email', 'phone'}

SIGNED = False


class SignHome(Home):

    def web_login(self, redirect=None, **kw):
        res = super().web_login()
        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        # print(SIGN_UP_REQUEST_PARAMS)
        phone = values.get('phone')
        # print('________________2 ', phone)
        # validates the phone number
        if 'phone' in values:
            if len(phone) != 11:
                raise UserError(_("Phone Number is not valid please retype it."))

            for number in phone:
                if ord(number) >= 48 and ord(number) <= 57:
                    pass
                else:
                    raise UserError("Phone Number is not valid; please retype it.")

            if phone[0] != '0' or phone[1] != '1':
                raise UserError(_("Phone Number is not valid; please retype it."))

            if phone[2] != '0' and phone[2] != '1' and phone[2] != '2' and phone[2] != '5':
                raise UserError(_("Phone Number is not valid; please retype it."))
            global SIGNED
            SIGNED = True

        return res


class SignupForm(AuthSignupHome):


    def do_signup(self, qcontext):
        if not SIGNED:
            return
        res = super(SignupForm, self).do_signup(qcontext)
        return res
