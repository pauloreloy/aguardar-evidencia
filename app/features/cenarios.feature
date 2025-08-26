# language: pt
Funcionalidade: Recepcao de arquivo

@cenario.1
Cenário: 1 Arquivo recebido com sucesso
    Dado que é recebido evento do sqs sqs-receber-conteudo
    | $.*[0].messageId                      |
    | d3340660-a906-4f41-ac1f-525e62cd8320  | 
    Quando a função lambda é executada com
    | feature_toggle_circuit_breaker | 
    | false                          |
    Entao a função lambda não gera exceções