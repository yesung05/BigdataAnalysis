import ollama

response = ollama.generate(
    model = 'gemma3:4b',
    prompt = 'What is the capital of South Korea?'
)

print(response['message']['content'])