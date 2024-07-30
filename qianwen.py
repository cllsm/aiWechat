import requests
import json
from prompt import *


def get_msg(user_content):
    url = "http://localhost:8000/v1/chat/completions"
    # 假设这是您要发送的数据
    print(user_content)
  # 构建 payload
    payload = {
        "model": "qwen",
        "messages": [
            {
                "role": "user",
                "content": user_content
            }
        ],
        "stream": False
    }

    # 添加额外的上下文信息
    context = {
        "role": "system",
        "content": init_history[0]
    }
    payload['messages'].insert(0, context)  # 将上下文信息插入到第一条消息前

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer _jtCqavMyTlqjs4Jl0Fce3oGBnSgLPzeCmIPYRetreMU*Ent6AHvLFvsFhJ_nw9v0'
    }

    # 将 payload 转换为 JSON 格式
    json_payload = json.dumps(payload)

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=json_payload)
    print(response.status_code)
    if response.status_code == 200:
        # 解析响应的 JSON 数据
        response_data = json.loads(response.text)
        
        # 获取回复的内容
        content = response_data['choices'][0]['message']['content']
        
        # 打印回复内容
        print(content)
        
        # 添加收到的回复到 messages 列表中
        # payload['messages'].append({
        #     "role": "assistant",
        #     "content": content
        # })
        
        return content
    else:
        # 如果响应状态不是200，则打印错误信息
        print(f"Failed to get a response: {response.status_code}")
        return '响应失败'
    