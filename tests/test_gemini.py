# Add Google Gemini AI support.
# pip install google-generativeai

import os
from google import genai
from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/apps/iagent/.env'), verbose=True)
os.environ.pop('GOOGLE_API_KEY', None) # Default use GOOGLE_API_KEY, remove it in
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL='gemini-2.5-pro-preview-06-05'
client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
  model=MODEL,
  contents="What is the meaning of life?"
)
print(response.text)
exit(0)

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    ),
)

