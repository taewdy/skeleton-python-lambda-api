terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "photos_api" {
  filename         = "function.zip"
  function_name    = "photos-api"
  role             = aws_iam_role.lambda_role.arn
  handler          = "src.handlers.get_photos_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("function.zip")

  environment {
    variables = {
      PYTHONPATH = "/var/task/src"
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "photos_api_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_api_gateway_rest_api" "photos_api" {
  name        = "photos-api"
  description = "Photos API Gateway"
}

resource "aws_api_gateway_resource" "photos" {
  rest_api_id = aws_api_gateway_rest_api.photos_api.id
  parent_id   = aws_api_gateway_rest_api.photos_api.root_resource_id
  path_part   = "photos"
}

resource "aws_api_gateway_method" "get_photos" {
  rest_api_id   = aws_api_gateway_rest_api.photos_api.id
  resource_id   = aws_api_gateway_resource.photos.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.photos_api.id
  resource_id = aws_api_gateway_resource.photos.id
  http_method = aws_api_gateway_method.get_photos.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.photos_api.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.photos_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.photos_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [aws_api_gateway_integration.lambda]

  rest_api_id = aws_api_gateway_rest_api.photos_api.id
  stage_name  = "prod"
} 