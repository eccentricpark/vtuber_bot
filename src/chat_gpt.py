from src.config.libaray_config import get_openai_object

async def generate_chat_completion(prompt, model="vtuber_test", temperature=1, max_tokens=200):
    current_messages = prompt
    openai = get_openai_object()
        
    response = openai.ChatCompletion.create(
        engine=model,
        messages=current_messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    result = response['choices'][0]['message']['content']
    return result