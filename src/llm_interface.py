import openai
import json
import os
from typing import Dict, List, Tuple

class LLMInterface:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        
    def analyze_problem(self, description: str) -> Dict:
        """Analyze geometric problem using LLM"""
        prompt = f"""
        Analyze the following geometric problem and extract key components:
        {description}
        
        Please identify:
        1. Given conditions
        2. What needs to be proved
        3. Key geometric entities
        4. Known relationships
        
        Format the response as JSON.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"LLM API call failed: {str(e)}")
            return {}