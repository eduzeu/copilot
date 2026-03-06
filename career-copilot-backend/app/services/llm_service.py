import os 
import anthropic
from typing import Optional 

client = anthropic.Client(os.getenv("AI_KEY"))

MODEL = "claude-sonnet-4-6"

def call_llm(prompt:str, system_prompt: Optional[str] = None, max_tokens: int = 1024) -> str: 
  '''
  send a prompt to the LLM and return the response 

  Args: 
      prompt: the user message to send
      system_prompt: an optional system prompt to provide context to the LLM
      max_tokens: the maximum number of tokens to generate in the response

  Returns:
      the response from the LLM as a string
    
  Raises: 
       anthropic.APIConnectionError: If the API is unreachable
        anthropic.AuthenticationError: If the API key is invalid
        anthropic.RateLimitError: If rate limit is exceeded
  '''

  messages = [{"role": "user", "content": prompt}]

  kwargs = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": messages,
    }
  
  if system_prompt:
    kwargs["system"] = system_prompt
  
  response = client.chat.completions.create(**kwargs)
  return response.choices[0].message.content


def call_llm_json(prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 1024) -> dict:
    '''
    send a prompt to the LLM and return the response as a JSON object

    Args:
        prompt: the user message to send
        system_prompt: an optional system prompt to provide context to the LLM
        max_tokens: the maximum number of tokens to generate in the response

    Returns:
        the response from the LLM as a JSON object
    
    Raises: 
       anthropic.APIConnectionError: If the API is unreachable
        anthropic.AuthenticationError: If the API key is invalid
        anthropic.RateLimitError: If rate limit is exceeded
    '''

    json_instructions = "Respond only with a JSON object. Do not include any text outside of the JSON. The JSON should be properly formatted and parsable."
    combined_system_prompt = f"{system_prompt}\n\n{json_instructions}" if system_prompt else json_instructions

    return call_llm(prompt, system_prompt=combined_system_prompt, max_tokens=max_tokens)
    