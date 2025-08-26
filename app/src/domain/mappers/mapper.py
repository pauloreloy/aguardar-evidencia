import json
from src.config import params


class Mapper:

    
    def __init__(self, mapper_schema: str, inverse: bool = False):
        self.mapper_schema = mapper_schema
        self.schema = self.load()
        if inverse:
            self.schema = {v: k for k, v in self.schema.items()}


    def load(self):
        mapper_file = f"{params.MAPPER_PATH}/{self.mapper_schema}_mapper.json"
        try:
            with open(mapper_file, 'r') as file:
                schema = json.loads(file.read())
            return schema
        except FileNotFoundError:
            print(f"Mapper schema file {self.mapper_schema} not found.")
            return None
        except Exception as e:
            print(f"An error occurred while loading the mapper schema: {e}")
            return None
    

    def map(self, data: dict):
        if not self.schema:
            return data
        mapped = {}
        for k, v in data.items():
            mapped_key = self.schema.get(k)
            if mapped_key:
                mapped[mapped_key] = v
            else:
                mapped[k] = f"notmapped:{v}"
        return mapped