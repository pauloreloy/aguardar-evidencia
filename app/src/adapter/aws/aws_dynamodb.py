
from src.adapter.aws.aws_config import AWSConfig


class DynamoDB:

    
    def __init__(self):
        self.client = AWSConfig("dynamodb").get_resource()
    

    def list_tables(self):
        response = self.client.tables.all()
        return [table.name for table in response]
    
    
    def put_item(self, table_name: str, item: dict):
        table = self.client.Table(table_name)
        response = table.put_item(Item=item)
        return response


    def get_item(self, table_name: str, key: dict):
        table = self.client.Table(table_name)
        response = table.get_item(Key=key)
        return response.get('Item', None)
    
    
    def query_item(self, table_name: str, pk_name: str, pk_value):
        table = self.client.Table(table_name)
        response = table.query(
            KeyConditionExpression=f"{pk_name} = :pk_value",
            ExpressionAttributeValues={":pk_value": pk_value}
        )
        return response.get('Items', [])


    def update_item(self, table_name: str, key: dict, update_expression: str, expression_attribute_values: dict):
        table = self.client.Table(table_name)
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response


    def update_table_data(self, table_name: str, key: dict, data: dict):
        table = self.client.Table(table_name)
        update_expression_parts = []
        expression_attribute_values = {}
        for k, v in data.items():
            placeholder = f":{k}"
            update_expression_parts.append(f"{k} = {placeholder}")
            expression_attribute_values[placeholder] = v

        update_expression = "SET " + ", ".join(update_expression_parts)
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        return response


    def insert_item(self, table_name: str, item: dict):
        table = self.client.Table(table_name)
        response = table.put_item(Item=item)
        return response