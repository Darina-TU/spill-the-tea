import os
from openai import OpenAI
from configs import config
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

response = client.responses.create(
    model=config.MODEL_NAME,
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)