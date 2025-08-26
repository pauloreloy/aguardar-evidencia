
from src.adapter.aws.aws_client                 import AWS
from src.domain.exceptions.usecase_exceptions   import EvidenciaNaoRegistradaException
from src.config                                  import params
import json


class SalvarPayloadUseCase:


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def execute(self, payload: dict, dados_s3: dict):
        self.aws_client.s3_client.put_object(
            bucket  = dados_s3.get("s3_bucket"),
            key     = dados_s3.get("s3_key"),
            data    = json.dumps(payload).encode('utf-8')
        )
       