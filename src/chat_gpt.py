from src.config.libaray_config import get_openai_object

# Azure의 Chat GPT API를 연결하여 GPT4가 답변하도록 설정
async def generate_chat_completion(prompt, model="vtuber_test", temperature=1, max_tokens=200):
    current_messages = prompt
    openai = get_openai_object()

    # 컨텍스트 메시지 출력
    print("Current messages (context):")
    for message in current_messages:
        print(f"Role: {message['role']} - Content: {message['content']}")

    response = openai.ChatCompletion.create(
        engine=model,
        messages=current_messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    if response['choices'][0].get('finish_reason') == 'content_filter':
        print("Content filtered by OpenAI.")
        assistant_content = "필터링"  # 필터링된 경우의 기본 응답
    else:
        assistant_content = response['choices'][0]['message']['content']

    return assistant_content