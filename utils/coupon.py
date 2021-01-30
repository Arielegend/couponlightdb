class Coupon(object):
    """
    Coupon object
    ~~~~~~~~~~
    Simple class for Coupon object
    """
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

    def coupon_push_msg(self, exists: bool) -> str:
        """
        Args:
            exists: a boolean indicates if coupon exist in table or no
        Returns:
              String message, weather coupon was uploaded to table, or already exists
        """
        if exists:
            return f"Coupon  --  code: {self.code}, domain: {self.domain} --  already exists!"
        else:
            return f"Successfully added new coupon: (code: {self.code}), (value: {self.value}), (domain: {self.domain})"
