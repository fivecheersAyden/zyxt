import asyncio
import websockets
import json
import requests

async def chat(websocket, path):
    async for user_input in websocket:
        user_input = """
你是一个智能英语学习助手，我会给你一个JSON数据，里面包含了用户需要你分析的英语题目，
请根据题目信息和用户的作答，给出详细的评分和解析，格式如下：
{
    "得分": "xxx/xxx",
    "评价": “”，
    "解析": {
        "语法": "",
        "词汇": "",
        "拼写": ""
    }
}
我只要json格式的返回，请不要给我输出其他信息。

""" + user_input
    
        final_input = {
            "model": "generalv3.5",
            "messages": [{"role": "user", "content": user_input}],
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

start_server = websockets.serve(chat, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
