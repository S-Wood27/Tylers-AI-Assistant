from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to OpenAI
client = OpenAI()

# Send a test message
response = client.responses.create(
    model="gpt-5.5",
    input="Say hello to Chloe in one sentence."
)

# Print the response
print(response.output_text)