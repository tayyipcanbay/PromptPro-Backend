import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

# Now you can access the environment variables as before
api_key = os.getenv('OPENAI_API_KEY')

def run_query(api_key, query, model="gpt-3.5-turbo-instruct", temperature=0.5, max_tokens=1000, top_p=1):
    """
    Run a query against the specified model and return the response.

    Parameters:
    api_key (str): The API key for OpenAI.
    query (str): The query to run against the model.
    model (str): The model to use for the query.
    temperature (float): The temperature to use for the query.
    max_tokens (int): The maximum number of tokens to generate.
    top_p (float): The nucleus sampling (top_p) to use.

    Returns:
    response: The response from the model.
    """
    client = OpenAI(api_key=api_key)
    # try:
    response = client.completions.create(
        model=model,
        prompt=query,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    # Extract necessary information from the response
    response_data = {
        'id': response.id,
        'object': response.object,
        'created': response.created,
        'model': response.model,
        'choices': [{'text': choice.text, 'finish_reason': choice.finish_reason} for choice in response.choices]
    }
    return response_data.get('choices')[0].get('text')