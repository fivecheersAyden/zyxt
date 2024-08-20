# 实现口语练习
# 前端先发送场景，用户角色，gpt角色，主线
import asyncio
import websockets
import urllib.parse
import json
import requests
import re

def split_string(text):
    # 定义标点符号列表
    punctuation = ['。', '：', '，', '！', '？', ',', '!', '?', ':', '.']

    # 使用正则表达式将字符串按标点符号拆分，并保留标点符号
    split_result = re.split(r'([。：，！？,!?:.])', text)

    # 去除空字符串
    result = [part for part in split_result if part]

    return result

def call_llm(prompt):
    # client = OpenAI(
    #     api_key=api_key,
    # )
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.choices[0].message.content.strip()

    final_input = {
        "model": "generalv3.5",
        "messages": [{"role": "user", "content": prompt}]
    }
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = final_input
    header = {
        "Authorization": "Bearer e7fc4e9b8b7702173a8d0d04e758bca8:Y2YzMTE1Y2FmNTY1YTMxYzJmM2M4ZGQ2"  # 注意此处替换自己的key和secret
    }
    response = requests.post(url, headers=header, json=data)
    for line in response.iter_lines(decode_unicode="utf-8"):
        print(line)
        lineJson = json.loads(line)
        return lineJson["choices"][0]["message"]["content"]
        # if line == "data: [DONE]":
        #         # await websocket.send("DONE")
        #         break
        # if len(line) > 2:
        #     cleanedLine = line.replace("data:", "", 1);
        #     lineJson = json.loads(cleanedLine)
        #     content = lineJson["choices"][0]["delta"]["content"]
        #     # await websocket.send(content)
        #     return content
    

start_data = {
    "scene": "旅游问路",
    "user_role": "游客",
    "gpt_role": "附近居民",
    "main_line": "此时用户想要前往海边，但是不知道具体的路线，需要向附近居民询问"
}

optimize_propmt = """
You are a good Prompt Engineer (Prompt Engineer), you are familiar with [CRISPE Prompt Framework] and are good at transforming regular Prompts into good Prompts that conform to [CRISPE Prompt Framework] and make chatGPT output responses that meet expectations.

The steps to transform [CRISPE Prompt Framework] are as follows:
1. Roles and Competencies: Based on my question (Prompt), think of 1 or more roles that chatGPT is best suited to play, which should be the most senior expert in the field and best suited to solve my question.
2. Contextualization: Based on my problem (Prompt), think about why I am asking this question and state the reason, background, and context in which I am asking it.
3. Task Statement: Based on my question (Prompt), think of a list of tasks that I need to give to chatGPT to complete in order to solve my question.
4. Output Format: Based on my problem (Prompt), think about what kind of output format or text style is the most suitable, such as MarkDown, List, Table, Json, Dialog, Prose, Poetry.... This format should facilitate the presentation of results.
5. Example request: Based on my question (Prompt), ask chatGPT to provide several different examples for better explanation.
6. Optimize Prompt: Based on what you have thought about in steps 1-5, pretend you are me, help me ask chatGPT a question, express my request completely, and output [Optimize Promot].

Here's an example based on the [CRISPE Prompt framework] and outputting [Optimize Promot]:
{{
**Original Prompt**: "Is there a good way to crawl information from a web page?"

The transformation process is as follows:
1.**Roles and Capabilities**: the most suitable role for ChatGPT in this scenario would be a computer science expert familiar with web crawling and information extraction. In addition, since ChatGPT can extract and analyze information from large amounts of text, it can also assume the role of a data scientist.
2.**CONTEXT STATEMENT**: I may be crawling data from web pages for a particular study, or I may be a beginner who is learning web crawling techniques. Regardless of my context and purpose, I would like to find an effective way to crawl data from web pages.
3.**Task Statement**: Based on the questions I have posed, the following tasks need to be presented to ChatGPT: Provide one or more methods for crawling information from web pages, including but not limited to the tools used, programming languages, and operational steps; discuss the advantages and disadvantages of these methods; and provide real-world examples of the use of these methods.
4.**Output Format**: Considering that this is a technical issue, the most suitable output format should be a clear, structured list of steps, which can be in Markdown format, accompanied by code examples.
5.**Case Requirements**: ChatGPT is required to provide at least two different methods of crawling web page information and provide a detailed example for each method.
6.**Optimization Prompt**:
You are a computer science expert specializing in web crawling and information extraction, and you are also a data scientist who specializes in extracting and analyzing information from large amounts of text. I need to crawl data from web pages, either for research or to learn web crawling techniques, and I would like to find an effective way to do so. Please combine your expertise and provide one or more methods for crawling information from web pages, including but not limited to the tools used, programming language, procedure, etc., and discuss the advantages and disadvantages of these methods. Please create a clear, structured list of steps for me using Markdown format with code examples. Finally, I would also like you to provide a detailed example for each method to help me better understand and apply them.
}}

Next I will give my question (Prompt), please follow my Prompt
1. optimize the prompt based on [CRISPE Prompt Framework] as per the above thinking, but only output the final [Optimized Prompt];
2.note that the final prompt you return should be in English

My prompt is as follows:
{}
"""

tip_prompt = """
任务：作为对话引导专家，你需要扮演一个能够引导用户进行深入表达或回答问题的角色。请根据以下聊天记录，提供一句话，引导用户进一步阐述他们的想法或回答，以促进对话的深入和更全面的理解。
注意：
（1）注意，你返回的提示应该合乎现实中的对话逻辑，即你返回的提示应当是合理的，如果用户采用了你的提示，其形成的对话，应当是一个日常正常的对话。
（2）你只需要返回提示即可，不可以返回提示以外的任何话
（3）你的提示应该是应该是一个引导，而不是一个问题
（4）返回的提示应当是中文，注意不要返回英文 !重要注意不要返回英文 !重要注意不要返回英文 !重要
返回的示例：
（1）可以详细描述一下你想要去的南海滩是在哪个城镇或城市。
（2）可以介绍一下你的爱好。
对话如下：
{}
"""


test = {
    "scene": "旅游问路",
    "user_role": "游客",
    "gpt_role": "附近居民",
    "main_line": "此时用户想要前往海边，但是不知道具体的路线，需要向附近居民询问",
    "msg": "用户对话问题",
    "historyDialogue": [{"type": "ai/usr", "content": "历史对话内容"}]
    }


# system_prompt = f"""You are an experienced oral trainer who focuses on simulating various dialogue scenarios to help users improve their oral expression skills. In this scenario, you will play the role of a nearby resident, while the user will play the role of a tourist. The background of the conversation is asking for directions during a trip. The user wishes to go to the beach but is unsure of the specific route, so they need to inquire with nearby residents. Please be fully prepared on how to guide tourists, including providing clear guidance, a friendly attitude, and necessary supplementary suggestions."""

async def echo(websocket, path):
    data = 1
    print("连接成功")
    # # 获得这次访问的用户id 错题id查询历史聊天记录
    # query = urllib.parse.urlparse(path).query
    # params = urllib.parse.parse_qs(query)
    # userId = params.get("userId", [""])[0]
    system_input = None

    async for message in websocket:
        history_chat = []
        print(message)
        message_json = json.loads(message)
        # 第一次连接进行处理
        if data == 1:
            # 第一次连接设置系统prompt
            data = data + 1
            # 只有第一次的时候才发送的场景信息
            my_prompt = f"现在需要你充当一个英语口语老师，你需要与用户进行口语对话，你们对话的场景是：{message_json['scene']}，需要你扮演{message_json['gpt_role']}，用户扮演{message_json['user_role']}，此时对话的主要内容是：{message_json['main_line']}"
            system_prompt = optimize_propmt.format(my_prompt)
            system_prompt = call_llm(system_prompt)
            print("====================system_prompt====================")
            print(system_prompt)
            print("====================system_prompt====================")
            system_input = {
                "role": "assistant",
                "content": system_prompt
            }

        history_chat.append(system_input)
        # 添加历史聊天记录
        for chat in message_json['historyDialogue']:
            # 进行映射
            if chat['type'] == 'ai':
                temp_chat = {
                    'role' : 'assistant',
                    'content' : chat['content']
                }
                history_chat.append(temp_chat)
            if chat['type'] == 'usr':
                temp_chat = {
                    'role' : 'user',
                    'content' : chat['content']
                }
                history_chat.append(temp_chat)
        if message_json['msg'] != "":
            # 判断是否是空的
            # 进行对话msg
            # user_input = {
            #     "role": "user",
            #     "content": message_json['msg']
            # }
            # history_chat.append(user_input)
            print(history_chat)
            url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
            data = {
                "model": "generalv3.5",
                "messages": history_chat,
                "stream": True
            }
            header = {
                "Authorization": "Bearer e7fc4e9b8b7702173a8d0d04e758bca8:Y2YzMTE1Y2FmNTY1YTMxYzJmM2M4ZGQ2"  # 注意此处替换自己的key和secret
            }
            response = requests.post(url, headers=header, json=data, stream=True)
            collected_chunks = []
            collected_messages = []
            reply = ""
            for line in response.iter_lines(decode_unicode="utf-8"):
                if line == "data: [DONE]":
                    send_message = f'{{"type":"chat","content":"None"}}'
                    print(send_message)
                    await websocket.send(send_message)
                    break
                if len(line) > 2:
                    cleanedLine = line.replace("data:", "", 1);
                    print('cleanedLine: ', cleanedLine)
                    lineJson = json.loads(cleanedLine)
                    content = lineJson["choices"][0]["delta"]["content"]

                    result = split_string(content)
                    for i in result:
                        send_message = f'{{"type":"chat","content":"{i}"}}'
                        print(send_message)
                        await websocket.send(send_message)

                    if content != "None":
                        reply = reply + content
            
            print(reply)
            ai_chat = {
                "role": "assistant",
                "content": reply
            }
            # 回复的内容如下
            print(f"assistant:{reply}")
            history_chat.append(ai_chat)
            # 根据对话返回对应的提示
            exactly_tip_prompt = tip_prompt.format(str(history_chat))
            print("====================exactly_tip_prompt====================")
            print(exactly_tip_prompt)
            print("====================exactly_tip_prompt====================")

            exactly_tip = call_llm(exactly_tip_prompt)
            print("====================exactly_tip====================")
            print(exactly_tip)
            print("====================exactly_tip====================")
            # 将这个tip返送给前端
            send_tip = f'{{"type":"tip","content":"{exactly_tip}"}}'
            print(send_tip)
            tip = {
                "type":"tip",
                "content":exactly_tip
            }
            await websocket.send(send_tip)


start_server = websockets.serve(echo, "www.fivecheers.com", 1022)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
