import asyncio
import websockets
import json
import requests

async def chat(websocket, path):
    async for user_input in websocket:
        user_json = json.loads(user_input)
        final_messages = []
        final_messages.append({"role": "user", "content": "你好，你是一个AI英语教师，采用苏格拉底式的启发式的教学方法，不是直接告诉我答案，而是循循善诱，引导我逐步获取知识。后续的对话请围绕一道" + user_json["question_type"] + "引导式教学"})
        final_messages.append({"role": "assistant", "content": "好的，我会引导你逐步获取知识，而不是直接简单粗暴地填鸭式教学的告诉你答案，现在清告诉我你要询问的"+  user_json["question_type"] + "题是什么吧"})
        final_messages.append({"role": "user", "content": "这道题的题目是：" + user_json["question"] + "，我写的答案是" +  user_json["answer"]})
        for message in user_json["historyDialogue"]:
            final_messages.append(message)
        final_messages.append({"role": "user", "content": user_json["msg"]})

    
        final_input = {
            "model": "generalv3.5",
            "messages": final_messages,
            "stream": True
        }

        url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
        data = final_input
        header = {
            "Authorization": "Bearer e7fc4e9b8b7702173a8d0d04e758bca8:Y2YzMTE1Y2FmNTY1YTMxYzJmM2M4ZGQ2"  # 注意此处替换自己的key和secret
        }
        response = requests.post(url, headers=header, json=data, stream=True)

        # 流式响应解析示例
        response.encoding = "utf-8"
        for line in response.iter_lines(decode_unicode="utf-8"):
            if line == "data: [DONE]":
                    await websocket.send("DONE")
                    break
            if len(line) > 2:
                cleanedLine = line.replace("data:", "", 1);
                lineJson = json.loads(cleanedLine)
                content = lineJson["choices"][0]["delta"]["content"]
                await websocket.send(content)

start_server = websockets.serve(chat, "ws://www.fivecheers.com", 1026)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
