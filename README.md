# AWS Elastic Beanstalk Django DRF Starter

![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

# AWS Elastic Beanstalk Django DRF
Simple Django starter with DRF and ready for AWS Elastic Beanstalk.

## Create your stack on AWS
Running  ``` aws cloudformation create-stack --stack-name my-python-eb-stack --template-body file://template.json --capabilities CAPABILITY_IAM``` will create your stack using ``` template.json ``` on AWS.

## Getting Started
Running  ```./deploy.sh``` will create ```deploy.zip``` deployment package. 