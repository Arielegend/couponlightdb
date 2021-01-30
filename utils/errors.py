import json
from abc import abstractmethod

__TableDoesntExistMsg__ = "\nCoupons table doesnt exist. Try build it first using the build table button"
__GetCouponParamsMsg__ = "\nValue must be Integer in range [0,99].\nAnd domains name must be a bigger than 1"
__ReturnCouponsParamsMsg__ = "\nValue must be an Integer in range [0,99] \nAt least 1 coupon code, and a valid domain"


class Error(Exception):
    """
    Abstract Errors class
    there are currently 2 types of Errors:
        1. Params error
        2. DynamoDB error
    """
    @abstractmethod
    def msg(self):
        pass


class ParamsError(Error):
    """
    Represents wrong parameters given Errors
    """
    def __init__(self,  error_info):
        self.exec_info = error_info

    def msg(self):
        return f"Error: wrong Params error occured {self.exec_info}"


class DBError(Error):
    """
    Represents Dynamo DB Errors
    """
    def __init__(self,  error_info):
        self.exec_info = error_info

    def msg(self):
        return f"Error: dynamo db error occured\n {self.exec_info}"


def check_getCoupon_inputs(value: str, domain: str) -> None:
    """
    Args:
        1. value: str
        2. domain: str
    Returns:
        boolean indicates if inputs to get coupon command are valid.
    Note:
        Checks the inputs for the return_coupons command
        i.e  -1 < int(value) < 100 AND domain is not an empty string
    Raise:
        Exception ParamsError
    """
    try:
        if 0 <= int(value) < 100 and len(domain) > 0:
            pass
        else:
            err = ParamsError(__GetCouponParamsMsg__)
            raise Exception(err.msg())
    except:
        err = ParamsError(__GetCouponParamsMsg__)
        raise Exception(err.msg())


def check_return_coupons_inputs(domain: str, value: str, codes: list) -> None:
    """
    Args:
        1. domain: str - the domain of the returned coupons
        2. value: str - the value of the returned coupons
        3. codes: list - the codes of the returned coupons
    Returns:
        boolean indicates if input to return coupons command is valid.
    Note:
        Checks the input for the return_coupons command
        Value must be Integer in range [0,99] and at least 1 coupon code should exist
    Raise:
        Exception ParamsError
    """
    try:
        if 0 <= int(value) < 100 and len(codes) > 0 and len(domain) > 0:
            pass
        else:
            err = ParamsError(__ReturnCouponsParamsMsg__)
            raise Exception(err.msg())
    except:
        err = ParamsError(__ReturnCouponsParamsMsg__)
        raise Exception(err.msg())


def check_code_without_spaces(code: str):
    """
    Args:
        1. code (str): the code we want to check
    Note:
        Fixing the codes input from the Return coupons form.
    Returns:
         Boolean if code contains any space notes in it
    """
    return '\n' in code or '\r' in code or '\t' in code


def check_get_response(response: dict) -> bool:
        """
        Args:
            1. response: the response we get from getting a coupon based on its domain and value
        Returns:
            booleans indicates if response is valid
        Raise:
            Exception in case response is bad
        """
        try:
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                pass

        except:
            err = DBError(str(json.dumpls(response)))
            raise Exception(err.msg())
