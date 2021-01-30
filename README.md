<h3 align="center">
Coupons server
</h3>

*** 

### Installation

<p> Make sure docker is running</p>
<p>Open a shell, pull  image</p>

* docker pull amazon/dynamodb-local 
* docker run -p 8000:8000 amazon/dynamodb-local
  * Additional info about this image can be found at https://hub.docker.com/r/amazon/dynamodb-local 
<p>Great! this light container will allow us to perform many dynamodb actions as we wish!</p>


* git clone https://github.com/Arielegend/couponlightdb.git
* cd couponlightdb
* python3 -m venv venv
* source venv/bin/activate
* pip install .


<p>Once pip finished, (at venv) run main.py file </p> 
 
<p>Flask server should open at local host, port 8000. </p>


http://127.0.0.1:8000/


### Usage
Service has 2 url endpoints:
* GET /

![Alt text](utils/images/Postman_get.png?raw=true "Title")

