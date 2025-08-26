
from src.adapter.aws.aws_client                 import AWS
from src.config                                 import params
from src.domain.usecases.salvar_payload_usecase import SalvarPayloadUseCase


class AguardarEvidenciaUseCase:


    step_name = "AGUARDAR_EVIDENCIA"


    def __init__(self, aws_client: AWS):
        self.aws_client = aws_client


    def execute(self, event: dict):
        payload = dict(event.get("Payload", {}).get("Payload", {}))
        numero_portabilidade = payload.get("numero_portabilidade")
        task_token = event.get("Payload", {}).get("TaskToken")
        execution_arn = event.get("Payload", {}).get("executionArn")
        execution_id  = execution_arn.split(":")[-1]
        dados_s3 = {
              "s3_bucket": params.BUCKET_PAYLOADS,
              "s3_key": f"payloads/{numero_portabilidade}/VALIDAR_DADOS#{execution_id}.json"
        }
        dat_cria = "2025-08-25T19:00:00Z"
        dat_exp = "2025-08-25T19:30:00Z"
        ttl_exp = 1766745000
        dados_tabela = {
            "tsk_tok":  task_token,
            "exe_arn":  execution_arn,
            "exe_id":   execution_id,
            "dat_cria": dat_cria,
            "dat_exp":  dat_exp,
            "ttl_exp":  ttl_exp,
            "pay_ref":  dados_s3
        }
        SalvarPayloadUseCase(self.aws_client).execute(payload, dados_s3)
        return self.aws_client.dynamodb_client.update_table_data(
            table_name  = params.TABELA_CONTROLE,
            key         = {
                params.PK_CONTROLE: numero_portabilidade,
                params.SK_CONTROLE: self.step_name
            },
            data = dados_tabela
        )
