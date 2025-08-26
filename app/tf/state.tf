{
  "Comment": "A description of my state machine",
  "StartAt": "Validar Retido",
  "States": {
    "Validar Retido": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:us-east-1:338966484167:function:lbd-validar-retido:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Necessário Evidência?",
      "OutputPath": "$.Payload"
    },
    "Necessário Evidência?": {
      "Type": "Choice",
      "Choices": [
        {
          "Next": "Enviar Retenção",
          "Variable": "$.necessarioEvidencia",
          "BooleanEquals": false
        }
      ],
      "Default": "Aguardar Evidência"
    },
    "Aguardar Evidência": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",
      "Parameters": {
        "Payload": {
          "TaskToken.$": "$$.Task.Token",
          "executionArn.$": "$$.Execution.Id",
          "Payload.$": "$"
        },
        "FunctionName": "arn:aws:lambda:us-east-1:338966484167:function:lbd-aguardar-evidencia:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Evidência Aceita",
      "Catch": [
        {
          "ErrorEquals": [
            "States.Timeout"
          ],
          "Next": "Validar Tentativas",
          "ResultPath": null
        }
      ],
      "TimeoutSeconds": 30
    },
    "Validar Tentativas": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:us-east-1:338966484167:function:lbd-validar-retry-evidencia:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Aguardar Evidência",
      "Catch": [
        {
          "ErrorEquals": [
            "EvidenciaNaoRegistradaException"
          ],
          "Next": "Evidência Não Registrada"
        }
      ]
    },
    "Evidência Aceita": {
      "Type": "Pass",
      "Next": "Enviar Retenção"
    },
    "Evidência Não Registrada": {
      "Type": "Pass",
      "End": true
    },
    "Enviar Retenção": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "OutputPath": "$.Payload",
      "Parameters": {
        "Payload.$": "$",
        "FunctionName": "arn:aws:lambda:us-east-1:338966484167:function:lbd-enviar-retencao:$LATEST"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "End": true
    }
  },
  "QueryLanguage": "JSONPath"
}