import logging
import responses
from src.event_sqs  import event_sqs 
from behave         import given, when, then
from jsonpath_ng    import jsonpath, parse


def step_dados(context):
    context.payload = event_sqs.copy()
    if context.table:
        for data in context.table:
            for key, value in data.items():
                jsonpath_expr = parse(f"$.{key}")
                for match in jsonpath_expr.find(context.payload):
                    path = match.full_path
                    path.update(context.payload, value)


@responses.activate
def step_executa_lambda(context):
    try:
        from lambda_function import lambda_handler
        context.exception = lambda_handler(context.payload, {})
    except Exception as e:
        context.exception = e
        logging.error(f"Erro ao executar lambda: {e}")


def step_verifica_excecao(context):
    if hasattr(context, 'exception'):
        assert isinstance(context.exception, Exception), f"Esperava uma exceção, mas não foi lançada: {context.exception}"
    else:
        assert False, "Nenhuma exceção foi capturada durante a execução da lambda."


@given('que é recebido evento do sqs sqs-receber-conteudo')
def step_impl(context):
    step_dados(context)


@when('a função lambda é executada com')
def step_impl(context):
    step_executa_lambda(context)


@then('a função lambda não gera exceções')
def step_impl(context):
    step_verifica_excecao(context)