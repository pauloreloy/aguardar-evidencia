
import json
from src.adapter.aws.aws_config import AWSConfig


class S3:

    
    def __init__(self):
        self.client = AWSConfig('s3').get_client()


    def put_object(self, bucket: str, key: str, data: bytes, **kwargs):
        self.client.put_object(
            Bucket=bucket, 
            Key=key, 
            Body=data,
            **kwargs
        )
