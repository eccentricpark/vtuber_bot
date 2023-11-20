import json


def read_json_file(file='../../mao.json'):
    with open(file, "r", encoding='UTF8') as f:
        data = json.load(f)      
    return data


def write_json(user_content, assistant_content):
    gpt_response = {
        "messages": [
            {
                "role": "system",
                "content": "당신은 트위치방송 유튜버 마오 입니다."
            },
            {
                "role": "user",
                "content": user_content
            },
            {
                "role": "assistant",
                "content": assistant_content
            }
        ]
    }
    with open("gpt_responses.jsonl", "a", encoding='UTF8') as file:
        json.dump(gpt_response, file, ensure_ascii=False)
        file.write(',\n')
        file.close()