import boto3
import logging
from src.config                 import params
from unittest.mock              import patch, MagicMock
from behave                     import fixture, use_fixture
from testcontainers.localstack  import LocalStackContainer


def str_to_bool(value):
    if isinstance(value, str):
        value = value.lower()
        if value in ('yes', 'true', 't', '1'):
            return True
        elif value in ('no', 'false', 'f', '0'):
            return False
    return bool(value) if value is not None else False

def localstack_fixture(context, **kwargs):

    context.localstack = LocalStackContainer(image='localstack/localstack:latest', 
                                             edge_port=4566, 
                                             region_name=params.AWS_REGION)
    context.localstack.start()
    session                         = boto3.session.Session()
    params.AWS_ENDPOINT             = context.localstack.get_url()
    params.AWS_ACCESS_KEY_ID        = params.LAMBDA_NAME
    params.AWS_ACCESS_SECRET_KEY    = params.LAMBDA_NAME

    context.sqs_client   = boto3.client(
        'sqs',
        endpoint_url            = context.localstack.get_url(),
        aws_access_key_id       = params.AWS_ACCESS_KEY_ID,
        aws_secret_access_key   = params.AWS_ACCESS_SECRET_KEY,
        region_name             = params.AWS_REGION
    )

    context.queue_url       = context.sqs_client.create_queue(QueueName="test_queue")['QueueUrl']
    params.SQS_QUEUE_URL    = context.queue_url

    yield context.localstack
    context.localstack.stop()


def before_all(context):
    use_fixture(localstack_fixture, context=context)


def fake_get_config(context, nome_da_configuracao, valor_padrao):
    if context.table is not None:
        for row in context.table:
            context.feature_toggle = f"{nome_da_configuracao}:{row.get(nome_da_configuracao)}\n {context.feature_toggle}"
            return row.get(nome_da_configuracao) if row.get(nome_da_configuracao) else valor_padrao
    return ""


def fake_is_enabled(context, nome_da_chave, valor_padrao):
    if context.table is not None:
        for row in context.table:
            context.feature_toggle = f"{nome_da_chave}:{row.get(nome_da_chave)}\n {context.feature_toggle}"
            return str_to_bool(row.get(nome_da_chave)) if row.get(nome_da_chave) else valor_padrao
    return False


def before_scenario(context, scenario):
    params.AWS_ENDPOINT = context.localstack.get_url()
    context.response = None
    context.feature_toggle = ""
    #context.get_config = patch('src.config.params.get_config', side_effect=fake_get_config).start()
    #context.is_enabled = patch('src.config.params.is_enabled', side_effect=fake_is_enabled).start()


def after_scenario(context, scenario):
    print("\n")
    #print(f"payload {context.payload}\n")
    #print(f"RetornoLambda {context.response}\n")
    #print(f"Feature Toggle {context.feature_toggle}")
    patch.stopall()
