import openai
import os
from dotenv import load_dotenv
# Define the tools the agent can use
import re
from agents import Agent, Runner

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment
my_api_key = os.getenv("OPENAI_API_KEY")

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write latest financial report for my trading of Tesla stock")

print(result.final_output)
