# Test in real environment

#### Install
* pip install boto3 moto
* pip install boto3 pymysql
* pip install boto3 mymysql moto

#### Run test

* python -m unittest discover -s . -p "Test3Manager.py"



#### AWS Secret Manager
* Create a secret on Aws Secret Manager
* Configure script to use credentials 
* Run the script and validate if data match.
#### MySQL
* Use a dockerized database
#### S3
* Create a bucket and all needed
* Test it the renaming action