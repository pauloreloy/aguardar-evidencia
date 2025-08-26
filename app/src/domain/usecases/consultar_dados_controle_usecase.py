from src.config                 import params
from src.domain.mappers.mapper  import Mapper
from src.adapter.aws.aws_client import AWS


class ConsultarDadosControleUseCase:


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def execute(self, pk: str, sk: str):
        get_result = self.aws_client.dynamodb_client.get_item(
            table_name  = params.TABELA_CONTROLE,
            key = {
                params.PK_CONTROLE: pk,
                params.SK_CONTROLE: sk
            }
        )
        if len(get_result) > 0:
            get_result = Mapper("database", True).map(get_result)
            return get_result
        return None