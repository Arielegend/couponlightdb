class Coupon(object):
    def __init__(self, params: dict):
        self.code = params['code']
        self.value = int(params['value'])
        self.domain = params['domain']

    def getCode(self):
        return self.code

    def getDomain(self):
        return self.domain

    def getValue(self):
        return self.value

    def coupon_push_msg(self, exist: bool):
        if exist:
            return f"Coupon  --  code: {self.code}, domain: {self.domain} --  already exists!"
        else:
            return f"Successfully added new coupon: (code: {self.code}), (value: {self.value}), (domain: {self.domain})"
