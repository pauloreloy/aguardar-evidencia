import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, os.pardir) # Go up one level to 'app'
sys.path.insert(0, app_dir)

from lambda_function import lambda_handler

class DummyContext:
    pass

if __name__ == "__main__":
    event_file_path = os.path.join(current_dir, "event_orquestracao.json")
    
    try:
        with open(event_file_path) as f:
            event = json.load(f)
        lambda_handler(event, DummyContext())
    except FileNotFoundError:
        print(f"Error: event_sqs.json not found at {event_file_path}")
        print("Please ensure 'event_sqs.json' is in the 'app/input/' directory.")
    except Exception as e:
        raise Exception(e)
