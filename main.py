from utils.coupon import Coupon
from utils.dynamo import DB
from flask import Flask, request, make_response, jsonify
from utils.errors import check_getCoupon_inputs, check_return_coupons_inputs, check_code_without_spaces

INTERNAL = 'internal'
app = Flask(__name__)

# Instancing DB object
dynamo_db = DB()

@app.route(f'/{INTERNAL}/GetCoupon', methods=['GET'])
def getCoupon():
    """
    Args:
        1. domain(str) : domain of coupon
        2. value(int): value of coupon
    Note:
        Command return coupon's code by a given domain and value
    Raise:
        Exception in case no such coupon is found
    """

    # Route is for GET method only
    if request.method == 'GET':
        domain = request.args.get('domain', type=str)
        value = request.args.get('value', type=int)

        # making sure inputs are valid
        check_getCoupon_inputs(value=value, domain=domain)

        # Setting value as its valid Integer
        value_fixed = int(value)

        # Fetching a single coupon by domain and value
        # Errors are handled at DB object
        response = dynamo_db.get_coupon_by_domain_and_value(domain=domain, value=value_fixed)

        return make_response(response)

    else:
        return 'Only GET request are allowed', 404


@app.route(f'/{INTERNAL}/ReturnCoupon', methods=['POST'])
def returnCoupons():
    """
    Args:
        1. domain (str): the domain for the returned codes
        2. value  (int): the value for the returned codes
        3. coupons (str) : the codes to push
    Note:
        For each coupon assigned, command will check if coupon exist in the table. (By code and domain)
        If not - coupon will be pushed to the table.
    Raise:
        Exception if table not exist
    """

    if request.method == 'POST':
        data = request.form.to_dict()

        # Fetching the data from post request.
        # Setting codes to be a list, created from input separated by space
        codes = data['codesreturn'].split(' ')
        domain = data['domainreturn']
        value = data['valuereturn']

        # Fixing spaces at codes input
        codes = [code for code in codes if len(code) > 0 and not check_code_without_spaces(code)]

        # making sure inputs are valid
        check_return_coupons_inputs(value=value, domain=domain, codes=codes)

        # For each of the codes we wish to push, we summery its results
        msgs = []
        for coupon_code in codes:
            coupon_to_add = Coupon({'domain': domain, 'value': value, 'code': coupon_code})

            # Making sure coupon not already exist
            if not dynamo_db.check_if_coupon_exist(code=coupon_code, domain=domain):
                # pushing coupon
                dynamo_db.put_item(coupon_to_add)
                msg = coupon_to_add.coupon_push_msg(exist=False)
            else:
                msg = coupon_to_add.coupon_push_msg(exist=True)

            msgs.append(msg)

        return jsonify(msgs)
    else:
        return 'Only POST request are allowed', 404


if __name__ == '__main__':
    app.run(debug=True, port=8000)
