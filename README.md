<h3 align="center">
Coupons server
</h3>

*** 

### Installation

<p> Make sure docker is running</p>
<p>Open a shell, pull  image</p>

* docker pull amazon/dynamodb-local 
  * ![Alt text](utils/images/Screenshot_1.png?raw=true "Title")

<br>

* docker run -p 8000:8000 amazon/dynamodb-local
  * ![Alt text](utils/images/Screenshot_2.png?raw=true "Title")

<br>

#### In a different shell run: 

* git clone https://github.com/Arielegend/couponlightdb.git
* cd couponlightdb
* python3 -m venv venv
* source venv/bin/activate
* pip install .


<p>Once pip finished, (at venv) run main.py file  

Flask server should open at local host, port 8000. </p>


http://127.0.0.1:8000/


### Usage
Service has 2 url endpoints:
* GET /GetCoupon 
  * Argument as follows:
    * 127.0.0.1:5000/internal/GetCoupon?domain=domain&value=value  

![Alt text](utils/images/postman_get.png?raw=true "Title")


* POST /ReturnCoupon
  * post with ***form-data*** as follows:
    * 'codesreturn': str, 'domainreturn': str, 'valuereturn': int

![Alt text](utils/images/postman_post.png?raw=true "Title")



***
* Additional info about amazon/dynamodb-local can be found at https://hub.docker.com/r/amazon/dynamodb-local 

