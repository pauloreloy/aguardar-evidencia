from src.config                                     import env_config,params
from src.domain.enums.log_level                     import LogLevel
from src.domain.enums.logger_message                import LoggerMessageEnum
from src.adapter.aws.aws_client                     import AWS
from src.common.correlation                         import set_correlation_id
from src.domain.decorators.exception                import exception_decorator
from src.domain.usecases.aguardar_evidencia_usecase import AguardarEvidenciaUseCase
from src.domain.exceptions.usecase_exceptions       import EvidenciaNaoRegistradaException

aws_client = AWS()


@exception_decorator(aws_client)
def process_event(event: dict):
    return AguardarEvidenciaUseCase(aws_client).execute(event)


def lambda_handler(event, context):
    if event.get("validarTentativas"):
        if event.get("controleTentativas", 0) >= params.NUMERO_MAXIMO_TENTATIVAS:
            raise EvidenciaNaoRegistradaException("Evidência não registrada")
        process_event(event)
        return event | {"controleTentativas": event.get("controleTentativas", 0) + 1}
    else:
        set_correlation_id(None)
        aws_client.logs_client.log(
            log_level=LogLevel.INFO,
            log_code=LoggerMessageEnum.L_1000
        )
        return process_event(event)
