from openai import OpenAI
# Initialize OpenAI client

client = OpenAI(
    api_key='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'
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
    ]
)

print(response.choices[0].message.content)
