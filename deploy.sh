#!/bin/bash
cd src; zip -r ../deploy.zip .
cd ..
aws s3 cp ./deploy.zip s3://code-aw3421341
aws elasticbeanstalk create-application-version --application-name my-python-eb-stack-sampleApplication-1DX82DSKJHJDO --version-label YourVersionLabel --source-bundle S3Bucket="code-aw3421341",S3Key="deploy.zip" --region="us-west-2"
aws elasticbeanstalk update-environment --application-name my-python-eb-stack-sampleApplication-1DX82DSKJHJDO --environment-name my-p-samp-1UU7OVWMR6BQ6 --version-label YourVersionLabel
