<h2 align="center">
Coupons server
</h2>

<p>Welcome to my coupons service using AWS DynamoDB light container</p>
<p>This service will allow u own your own amazing coupons service!</p>
<p>Just Enter as many coupons by domain_name, coupon_value(must be positive integer less than 100), and a coupon_code</p>
<p>See usage via postman at the buttom</p>


## Installation

<p>(Make sure docker is running)</p>
<p>Open a shell, pull  image:</p>

* docker pull amazon/dynamodb-local 
  * docker images
  * ![Alt text](utils/images/screenshot_1.png?raw=true "Title")
  * Additional info about amazon/dynamodb-local can be found at https://hub.docker.com/r/amazon/dynamodb-local 

<br>

* docker run -p 8000:8000 amazon/dynamodb-local
  * ![Alt text](utils/images/screenshot_2.png?raw=true "Title")
  * This container will allow us to perform dynamo DB actions.

<br>

#### In a different shell run: 

* git clone https://github.com/Arielegend/couponlightdb.git
* cd couponlightdb
* python3 -m venv venv
* source venv/bin/activate
* pip install .


#### Once pip finished

* (at venv) run main.py file
* Flask server should open at a local host, port 8000. 
* http://127.0.0.1:8000/
  * ![Alt text](utils/images/running_8000.png?raw=true "Title")


<br >

## Usage
Coupons service has 2 url endpoints:
* GET /GetCoupon 
  * Params: domain: str, value:int (lower than 100)
    * http://127.0.0.1:8000/internal/GetCoupon?domain=domain&value=20

![Alt text](utils/images/postman_get.png?raw=true "Title")


* POST /ReturnCoupon
  * Post with body as follows:
    * {'codesreturn': str, 'domainreturn': str, 'valuereturn': int}

![Alt text](utils/images/postman_post.png?raw=true "Title")


<br> 

***

<br> 


* <b>Post</b> example:
  * http://127.0.0.1:8000/internal/ReturnCoupon
  * {
   "codesreturn":"code1 code2 code3",
   "domainreturn":"domainX",
   "valuereturn":"10" 
    }
  * Responses examples:
    
            response = [
            "Successfully added new coupon: (code: code1), (value: 10), (domain: domainX)",
            "Successfully added new coupon: (code: code2), (value: 10), (domain: domainX)",
            "Successfully added new coupon: (code: code3), (value: 10), (domain: domainX)"
            ]
    
             response = [
                "Coupon  --  code: code1, domain: domainX --  already exists!",
                "Coupon  --  code: code2, domain: domainX --  already exists!",
                "Coupon  --  code: code3, domain: domainX --  already exists!"
             ]

<br >

* <b>Get</b> example:
  * http://127.0.0.1:8000/internal/GetCoupon?domain=domainAlpha&value=10
  * Responses examples :
    
        //Coupon exists 
            response = {
            'response_code': True,
            'coupon_code': 'code1' }
    
        //Coupon doesn't exists 
            response = {
            'response_code': False,
            'coupon_code': 'No such coupon' }

<br > 

