import copy
from src.config                                     import env_config
from src.domain.enums.log_level                     import LogLevel
from src.domain.enums.logger_message                import LoggerMessageEnum
from src.adapter.aws.aws_client                     import AWS
from src.common.correlation                         import set_correlation_id
from src.domain.decorators.exception                import exception_decorator
from src.domain.usecases.aguardar_evidencia_usecase import AguardarEvidenciaUseCase


aws_client = AWS()


@exception_decorator(aws_client)
def process_event(event: dict):
    return AguardarEvidenciaUseCase(aws_client).execute(event)


def lambda_handler(event, context):
    set_correlation_id(None)
    aws_client.logs_client.log(
        log_level=LogLevel.INFO,
        log_code=LoggerMessageEnum.L_1000
    )
    return process_event(event)
