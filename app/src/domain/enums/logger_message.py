import enum


class LoggerMessageEnum(enum.Enum):

    L_1000          = ("L_1000", "Iniciando lambda")
    L_1001          = ("L_1001", "Produzido mensagem Kafka")
    L_1002          = ("L_1002", "Erro ao produzir mensagem Kafka")
    LAMBDA_ERROR    = ("LAMBDA_ERROR", "Erro na execucao da lambda")

    def __init__(self, codigo: str, descricao: str):
        self.codigo = codigo
        self.descricao = descricao


    def __str__(self):
        return f"{self.codigo}: {self.descricao}"