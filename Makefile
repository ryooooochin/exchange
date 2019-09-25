BUCKET_NAME := xxxxx-bucket-for-deploy 
STACK_NAME := xxxxx-exchange 

bucket:
	aws s3 mb s3://${BUCKET_NAME} --region ap-northeast-1 

pac:
	aws cloudformation package \
	--template sam-template.yml \
	--output-template-file sam-output.yml \
	--s3-bucket ${BUCKET_NAME} 

deploy:
	aws cloudformation deploy \
	--template-file sam-output.yml \
	--stack-name  ${STACK_NAME} \
	--capabilities CAPABILITY_IAM 

all: pac deploy
