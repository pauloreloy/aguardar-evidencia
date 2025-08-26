
import json
from src.adapter.aws.aws_config import AWSConfig


class SecretsManager:

    
    def __init__(self):
        self.client = AWSConfig('secretsmanager').get_client()

    
    def get_secret_value(self, secret_id: str):
        response = self.client.get_secret_value(SecretId=secret_id)
        return json.loads(response.get("SecretString"))

