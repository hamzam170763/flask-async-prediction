import time
import random
from typing import Dict

def mock_model_predict(input: str) -> Dict[str, str]:
    # Simulate processing delay
    time.sleep(random.randint(8, 15))
    # Generate a random result
    result = str(random.randint(100, 10000))
    return {"input": input, "result": result}
