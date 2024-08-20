import asyncio
import websockets
import json
import requests
import time
import random
import pymysql
import urllib.parse

study_analysis_prompt = """
任务：现在需要你根据下面某个学生的信息，简要介绍该学生现在目前的英语学习情况。可以分为：英语语言理解，语言表达，语言知识三个维度，还有选择，阅读，翻译，作文四种题型的作答情况。
注意：
（1）你的角色是一个老师，你的回答应该是你基于下面的学生信息，对学生的学情进行分析。
（2）你现在正在面对面对学生的学情进行简要的分析，你的表达应当是和学生面对面交流，因此你的回答应当使用第二人称进行回答
（3）你的表达应当具有逻辑性，有理有据
（4）你的回答像是老师与学生之间对话一样，你要时刻记住你是一个英语老师，你现在正在对你的一个学生的近期学习情况进行分析。

用户的学习情况如下：
{}
"""

recommend_data = ""
redo_data = ""
analyse_data = []

no_recommed_data = "您今天没有需要巩固的习题。您可以尝试获取推荐的习题来复习知识！"

async def chat(websocket, path):
    query = urllib.parse.urlparse(path).query
    params = urllib.parse.parse_qs(query)
    print(params)
    userId = params.get("userId", [""])[0]


    history = [
        {
            "role": "assistant",
            "content": "您好，我是您的英语学习助手，帮助你解析英语错题和解答知识，有什么可以帮助您的？"
        }
    ]
    answering = False

    async for user_input in websocket:

        if user_input == "mode1": # 推荐习题2580
            # await send_stream(websocket, "定制内容1定，制内容1定制内容1定制内，容1定制内容1定制内容1定制内容1定制内容1。")
            getDataForRecommend(userId)
            test = recommend_data
            for char in test:
                await websocket.send(char)
                await asyncio.sleep(0.05)
            await websocket.send("DONE")
            ai_output = {"role": "assistant", "content": test}
            history.append(ai_output)
            
        elif user_input == "mode2": # 巩固之前的题目 7410
            # await send_stream(websocket, "定制内容2定制内容1定制内容1，定制内容1定制内容1定制内容1定制内容1定制内容，1定制内容1定制内容1定制内容1定制内容1。")
            getDataForRedo(userId)
            test = redo_data
            for char in test:
                await websocket.send(char)
                await asyncio.sleep(0.05)
            await websocket.send("DONE")
            ai_output = {"role": "assistant", "content": test}
            history.append(ai_output)
        elif user_input == "mode3": # 学情分析 1234
            # await send_stream(websocket, "定制内容3定制内容，1定制内容1定制内容1定制内容1定制内容1定制内容1定制内容1定制，内容1定制内容1定制内容1。")
            # 根据userId查询数据库，找到这个用户的详细信息
            # =================================================
            getDataForAnalyse(userId)
            user_info = str(analyse_data)
            analysis_prompt = study_analysis_prompt.format(user_info)
            url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
            final_input = {
                "model": "generalv3.5",
                "messages": [{"role": "user", "content": analysis_prompt}],
                "stream": True
            }
            header = {
                "Authorization": "Bearer e7fc4e9b8b7702173a8d0d04e758bca8:Y2YzMTE1Y2FmNTY1YTMxYzJmM2M4ZGQ2"  # 注意此处替换自己的key和secret
            }
            data = final_input
            response = requests.post(url, headers=header, json=data, stream=True)
            reply = ""
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
                    await asyncio.sleep(0.05)
                    if content != "None":
                        reply = reply + content
            
            print(reply)
            # 将AI的返回添加到数据库中
            ai_output = {"role": "assistant", "content": reply}
            history.append(ai_output)
        else:
            history.append({
                "role": "user",
                "content": user_input
            })

            final_input = {
                "model": "generalv3.5",
                "messages": history,
                "stream": True
            }

            url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
            data = final_input
            header = {
                "Authorization": "Bearer e7fc4e9b8b7702173a8d0d04e758bca8:Y2YzMTE1Y2FmNTY1YTMxYzJmM2M4ZGQ2"
                # 注意此处替换自己的key和secret
            }
            response = requests.post(url, headers=header, json=data, stream=True)

            # 流式响应解析示例
            response.encoding = "utf-8"
            for line in response.iter_lines(decode_unicode="utf-8"):
                if line == "data: [DONE]":
                    answering = False
                    await websocket.send("DONE")
                    break
                if len(line) > 2:
                    if not answering:
                        answering = True
                        history.append({
                            "role": "assistant",
                            "content": ""
                        })
                    cleanedLine = line.replace("data:", "", 1);
                    lineJson = json.loads(cleanedLine)
                    content = lineJson["choices"][0]["delta"]["content"]
                    history[len(history) - 1]["content"] += content
                    await websocket.send(content)


async def send_stream(websocket, str):
    time.sleep(1.5)
    for i in range(len(str)):
        await websocket.send(str[i])
        if random.random() < 0.8:
            time.sleep(random.uniform(0.03, 0.08))
        else:
            time.sleep(random.uniform(0.15, 0.2))
        if i == len(str) - 1:
            await websocket.send("DONE")
            break

def getDataForRecommend(userID):
    global recommend_data
    # 连接数据库，创建连接对象connection
    # 连接对象作用是：连接数据库、发送数据库信息、处理回滚操作（查询中断时，数据库回到最初状态）、创建新的光标对象
    connection = pymysql.connect(
        host="www.yym-free.com",
        user="jishe",
        password="jishe",
        db="jishe",
        port=3306,
    )
    cur = connection.cursor()
    # 获取用户的薄弱点数据
    cur.execute(
        "SELECT * from userskillscore where stuID=%s",
        (userID,),
    )
    cur2 = connection.cursor()
    # 获取用户的薄弱点数据
    cur2.execute(
        "SELECT * from question where stuID=%s",
        (userID,),
    )
    onequestion = cur2.fetchone()
    one = cur.fetchone()
    # 获取学生的所有薄弱点数据
    arr = [one[10], one[11], one[12], one[13]]
    # 对数据进行排序，并且保留原来的索引
    sorted_values, original_indices = sort_with_index(arr)
    # 用户还没问过问题
    if onequestion != None and sorted_values[3] == 0:
        recommend_data = "目前系统中还没有与您相关的历史提问记录，因此我们随机从题库中给您推荐了习题。如果这个不符合您的要求，可以重新让我生成！"
    # 用户问过问题 但是没上传过习题
    elif sorted_values[3] == 0:
        recommend_data = "我们基于您平时的提问记录，智能提取出关键知识点并分析您的学习水平，基于此我们从题库中抽取出适合您知识点的题目。如果这个不符合您的要求，可以重新让我生成！"
    # 只根据一个习题来推荐
    elif sorted_values[2] == 0:
        recommend_data = "根据您近一个月的提问记录，我了解到"
        recommend_data += (
            "您仅提问了"
            + str(one[original_indices[3] + 2])
            + "道"
            + getCategory(original_indices[3])
        )
        recommend_data += "。因此，您可能是在这种题型的解答上能力较差。我们基于题目的深层语义信息，给您推荐了以下习题。"
    else:
        recommend_data = "根据您近一个月的提问记录来分析，我们得出以下结论:"
        if one[2] != 0:
            recommend_data += "您一共提问了" + str(one[2]) + "道选择题，"
            recommend_data += "其中您的失分率为" + str(one[6]) + ";"
        if one[3] != 0:
            recommend_data += "您一共提问了" + str(one[3]) + "道阅读题，"
            recommend_data += "其中您的失分率为" + str(one[7]) + ";"
        if one[4] != 0:
            recommend_data += "您一共提问了" + str(one[4]) + "道翻译题，"
            recommend_data += "其中您的失分率为" + str(one[8]) + ";"
        if one[5] != 0:
            recommend_data += "您一共提问了" + str(one[5]) + "道作文题，"
            recommend_data += "其中您的失分率为" + str(one[9]) + ";"
        recommend_data += (
            "因此，我们推测您在"
            + getCategory(original_indices[3])
            + "题型上的表现最差，在"
            + getCategory(original_indices[2])
            + "题型上的表现次差。"
        )
        recommend_data += "因此，我们基于您历史提问记录中的问题，分析深层语义信息并给您推荐了以下习题。"
    connection.commit()
    connection.close()

def getDataForRedo(userID):
    global redo_data
    connection = pymysql.connect(
        host="www.yym-free.com",
        user="jishe",
        password="jishe",
        db="jishe",
        port=3306,
    )
    cur = connection.cursor()
    # 获取用户的巩固
    cur.execute(
        "select count(*),category from cuotiji where stuID=%s and needRedo=1 and (category!='yuedu' or sonProID is not null)GROUP BY category",
        (userID,),
    )
    all = cur.fetchall()
    if all == ():
        redo_data = "您今天没有需要巩固的习题。您可以尝试获取推荐的习题来复习知识！"
        return
    redo_data = "根据遗忘曲线和做题情况来综合分析后，我们得出以下结论：您一共需要复习"
    tmpdata = ""
    allnum = 0
    for one in all:
        allnum += one[0]
        tmpdata += str(one[0]) + "道" + getCategory2(one[1]) + "、"
    tmpdata = tmpdata[: len(tmpdata) - 1]
    redo_data += str(allnum) + "道习题。其中，包括" + tmpdata
    redo_data += "。您可以点击下面的按钮，快速跳转到错题巩固页面。"

def getDataForAnalyse(userID):
    global analyse_data
    connection = pymysql.connect(
        host="www.yym-free.com",
        user="jishe",
        password="jishe",
        db="jishe",
        port=3306,
    )
    cur = connection.cursor()
    # 获取用户的巩固
    cur.execute(
        "select * from levelrecord where stuID=%s order by startTime DESC limit 4",
        (userID,),
    )
    all = cur.fetchall()
    k = 0
    for one in all:
        # 如果数据为空，则没必要封装
        if one[3] != 0:
            item = {}
            analyse_data.append(item)
            analyse_data[k]["总体评分"] = one[3]
            analyse_data[k]["总体评价"] = one[4]
            analyse_data[k]["语言理解能力评分"] = one[6]
            analyse_data[k]["语言理解能力评价"] = one[7]
            analyse_data[k]["语言表达能力评分"] = one[8]
            analyse_data[k]["语言表达能力评价"] = one[9]
            analyse_data[k]["语言知识能力评分"] = one[10]
            analyse_data[k]["语言知识能力评价"] = one[11]
            analyse_data[k]["选择题表现评价"] = one[12]
            analyse_data[k]["选择题表现建议"] = one[13]
            analyse_data[k]["阅读题表现评价"] = one[14]
            analyse_data[k]["阅读题表现建议"] = one[15]
            analyse_data[k]["翻译题表现评价"] = one[16]
            analyse_data[k]["翻译题表现建议"] = one[17]
            analyse_data[k]["作文表现评价"] = one[18]
            analyse_data[k]["作文表现建议"] = one[19]
            k = k + 1

# 进行一个排序
def sort_with_index(arr):
    # 创建带有索引的元组列表
    indexed_arr = [(value, index) for index, value in enumerate(arr)]

    # 按照元素值进行排序
    indexed_arr.sort()

    # 提取排序后的值和对应的索引
    sorted_values = [item[0] for item in indexed_arr]
    original_indices = [item[1] for item in indexed_arr]

    return sorted_values, original_indices

# 根据索引来获取题型的名称
def getCategory(index):

    if index == 0:
        return "选择"
    elif index == 1:
        return "阅读"
    elif index == 2:
        return "翻译"
    else:
        return "作文"


# 根据拼音来获取题型的名称
def getCategory2(pinyin):

    if pinyin == "xuanze":
        return "选择"
    elif pinyin == "yuedu":
        return "阅读"
    elif pinyin == "fanyi":
        return "翻译"
    else:
        return "作文"

start_server = websockets.serve(chat, "www.fivecheers.com", 1021)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
