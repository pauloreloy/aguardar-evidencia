
from src.adapter.aws.aws_dynamodb       import DynamoDB
from src.adapter.aws.aws_logs           import Logs
from src.adapter.aws.aws_s3             import  S3

class AWS:


    def __init__(self):
        self.dynamodb_client        = DynamoDB()
        self.logs_client            = Logs()
        self.s3_client              = S3()