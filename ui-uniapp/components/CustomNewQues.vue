<template>
	<wd-config-provider theme="light">
		<div ref="newQuesContainer" class="new-ques-container">
			<!--题型选择-->
			<div class="ques-line" style="margin-bottom: -20px;">
				<div class="h1-line">
					<div class="h1">题型选择：</div>
					<div style="flex: 1;"></div>
					<!--选择器-->
					<div class="picker-container">
						<wd-picker :disabled="mode < 2" @confirm="selectCategory" z-index="999" v-model="customNewQues.category" :columns="quesTypeColumns" filterable></wd-picker>
					</div>
				</div>
			</div>
			<!--未选中，占位-->
			<div v-if="customNewQues.category === ''">
				<wd-skeleton :custom-style="{ width: '100%', margin: '36px 12px 0 12px' }" animation="gradient" theme="paragraph" />
				<wd-skeleton :custom-style="{ width: '100%', margin: '36px 12px 0 12px' }" animation="gradient" theme="text" />
				<wd-skeleton :custom-style="{ width: '100%', margin: '36px 12px 0 12px' }" animation="gradient" theme="paragraph" />
			</div>
			<!--作文翻译-->
			<div v-if="customNewQues.category === 'zuowen' || customNewQues.category === 'fanyi'">
				<!--题目-->
				<div class="ques-line dark-purple-card">
					<div class="h1">题目：</div>
					<div v-if="mode < 2">{{ customNewQues.content }}</div>
					<textarea v-else auto-height maxlength="-1" v-model="customNewQues.content" class="text-area"></textarea>
					<div v-if="mode == 2" class="btns-container">
						<button @click="ocrCommenSend('zuowen', 1001)"><wd-icon name="camera" size="20px"></wd-icon></button>
						<div></div>
					</div>
				</div>
				<!--我的作答-->
				<div class="ques-line dark-purple-card ques-line-card">
					<div class="h1">我的作答：</div>
					<div v-if="mode === 0">{{ customNewQues.stuAnswer }}</div>
					<textarea v-else auto-height maxlength="-1" v-model="customNewQues.stuAnswer" class="text-area"></textarea>
					<div v-if="mode > 0" class="btns-container">
						<button @click="ocrCommenSend('zuowen', 1002)"><wd-icon name="camera" size="20px"></wd-icon></button>
						<button v-if="!aiAnalysising" @click="aiAnalyseBtn()">分析本题</button>
						<button v-else >分析中</button>
					</div>
				</div>
				<!--智能分析-->
				<div class="ques-line">
					<div class="h1">智能分析：</div>
					<p>{{customNewQues.aiComment}}</p>
				</div>
			</div>
			<!--阅读选择-->
			<div v-if="customNewQues.category === 'yuedu' || customNewQues.category === 'xuanze'">
				<div class="ques-line">
					<!--文章-->
					<div class="ques-line">
						<div class="h1-line">
							<div class="h1" v-if="customNewQues.category === 'xuanze'">题目：</div>
							<div class="h1" v-if="customNewQues.category === 'yuedu'">文章：</div>
							<!-- <div class="tag-container">
								<div class="tag">{{customNewQues.category === 'xuanze' ? '选择' : '阅读'}}</div>
								<div class="tag" v-if="customNewQues.field !== undefined && customNewQues.field !== null && customNewQues.field">{{customNewQues.field}}</div>
							</div> -->
						</div>
						<textarea v-if="customNewQues.category === 'xuanze' && mode == 2" auto-height maxlength="-1" v-model="customNewQues.problem" class="text-area"></textarea>
						<div v-if="customNewQues.category === 'xuanze' && mode < 2">{{customNewQues.problem}}</div>
						<textarea v-if="customNewQues.category === 'yuedu' && mode == 2" auto-height maxlength="-1" v-model="customNewQues.content" class="text-area"></textarea>
						<div v-if="customNewQues.category === 'yuedu' && mode < 2">{{customNewQues.content}}</div>
						<div v-if="mode === 2" class="btns-container" >
							<button v-if="customNewQues.category === 'xuanze'" @click="ocrCommenSend('xuanze', 1003)"><wd-icon name="camera" size="20px"></wd-icon></button>
							<button v-if="customNewQues.category === 'yuedu'" @click="ocrCommenSend('yuedu', 1001)"><wd-icon name="camera" size="20px"></wd-icon></button>
							<div></div>
						</div>
					</div>
					<!--选择-->
					<div v-if="customNewQues.category === 'xuanze'">
						<!--选项-->
						<XuanzeCard :mode="mode < 2 ? 'normal' : 'insert'"
									:choice1="customNewQues.choice1" 
									:choice2="customNewQues.choice2"
									:choice3="customNewQues.choice3" 
									:choice4="customNewQues.choice4"
									:stuAnswer="customNewQues.stuAnswer"
									:answer="customNewQues.answer"
									@changeAnswer="(newAnswer)=>{customNewQues.answer = newAnswer}"
									@changeStuAnswer="(newAnwer)=>{customNewQues.stuAnswer = newAnwer}"></XuanzeCard>
						<!--AI分析-->
						<div v-if="mode > 0" class="sure-btn-container">
							<button v-if="!aiAnalysising" class="sure-btn" @click="aiAnalyseBtn()">分析本题</button>
							<button v-else class="sure-btn">分析中</button>
						</div>
						<!--智能分析-->
						<div class="ques-line">
							<div class="h1">智能分析：</div>
							<div>{{customNewQues.aiComment}}</div>
						</div>
					</div>
					<!--阅读-->
					<div v-if="customNewQues.category === 'yuedu'">
						<!--题目-->
						<div v-for="(exer, yueduIndex) in customNewQues.cuoTiList">
							<!--题目-->
							<div class="ques-line">
								<div class="h1">题目{{Number(yueduIndex+1)}}:</div>
								<div v-if="mode < 2">{{exer.problem }}</div>
								<textarea v-else auto-height maxlength="-1" v-model="exer.problem" class="text-area"></textarea>
							</div>
							<!--选项-->
							<XuanzeCard	:mode="mode < 2 ? 'normal' : 'insert'"
										:choice1="exer.choice1" 
										:choice2="exer.choice2"
										:choice3="exer.choice3" 
										:choice4="exer.choice4"
										:stuAnswer="exer.stuAnswer"
										:answer="exer.answer"
										@changeAnswer="(newAnswer)=>{exer.answer = newAnswer}"
										@changeStuAnswer="(newAnwer)=>{exer.stuAnswer = newAnwer}"></XuanzeCard>
							<!--删除本道-->
							<div v-if="mode === 2" class="btns-container" >
								<button @click="ocrCommenSend('xuanze', yueduIndex)"><wd-icon name="camera" size="20px"></wd-icon></button>
								<button @click="deleteXuanze(yueduIndex)"><wd-icon name="delete" size="20px"></wd-icon></button>
							</div>
							<!--智能分析-->
							<div class="ques-line" v-if="mode === 0">
								<div class="h1">智能分析：</div>
								<p>{{exer.aiComment}}</p>
							</div>
							<!--分割线-->
							<wd-divider style="margin: 12px 0;"></wd-divider>
						</div>
						<div v-if="mode === 2" class="sure-btn-container">
							<button class="sure-btn" style="background-color: #aaa;" @click="addXuanze()">新增选择</button>
						</div>
						<!--AI分析-->
						<div v-if="mode > 0" class="sure-btn-container">
							<button v-if="!aiAnalysising" class="sure-btn" @click="aiAnalyseBtn()">分析本题</button>
							<button v-else class="sure-btn">分析中</button>
						</div>
						<!--智能分析-->
						<div class="ques-line" v-if="mode > 0">
							<div class="h1">智能分析：</div>
							<p id="ai-comment">{{customNewQues.aiComment}}</p>
						</div>
					</div>
				</div>
			</div>
			<!--底部占位-->
			<div style="height: 48px;"></div>
		</div>
	</wd-config-provider>
	
</template>

<script setup>
	import { toRefs, defineProps, ref, defineExpose, onMounted, onBeforeUnmount, watch } from 'vue'
	import { globalProps } from '../js/global';
	import XuanzeCard from '@/components/XuanzeCard.vue'
	import socket from 'plus-websocket'
	import Vditor from 'vditor'
	import 'vditor/dist/index.css'
	
	const newQuesContainer = ref()
	const addXuanze = ()=>{
		customNewQues.value.cuoTiList.push({
                    "id": 78,
                    "category": null,
                    "problem": null,
                    "answer": null,
                    "sonProID": null,
                    "score": 0,
                    "choiceNum": 4,
                    "level": 0,
                    "field": null,
                    "knowledgeIDs": null,
                    "choice1": null,
                    "choice2": null,
                    "choice3": null,
                    "choice4": null,
                    "content": null,
                    "stuAnswer": null,
                    "aiComment": null,
                    "falseReason": null,
                    "userComment": null,
                    "sonExercise": null,
                    "cuoTiList": null,
                    "esID": null,
                    "single": false,
                    "existed": true
                })
	}
	const deleteXuanze = (index)=>{
		customNewQues.value.cuoTiList.splice(index, 1)
	}
	
	//使用父组件传递过来的值
	const props = defineProps({
	  customNewQues: JSON,
	  mode: Number //0只读 1做题 2编辑
	})
	const customNewQues = ref(JSON.parse(JSON.stringify(props.customNewQues)))
	//更改后通知对话
	watch(customNewQues, (newValue, oldValue) => {
	  uni.$emit('updateConversationQues',getAiChatJson())
	}, { deep: true });
	
	//更改子组件的customNewQues
	const updateCustomNewQues = (newQues)=>{
		customNewQues.value = newQues
	}
	//转换分析用JSON
	const getAiChatJson = ()=>{
		let postData = {
			question_type: '',
			question: '',
			user_answer: ''
		}
		switch(customNewQues.value.category){
			case 'zuowen':
				postData.question_type = '作文'
				postData.question = customNewQues.value.content
				postData.user_answer = customNewQues.value.stuAnswer
				break;
			case 'fanyi':
				postData.question_type = '翻译'
				postData.question = customNewQues.value.content
				postData.user_answer = customNewQues.value.stuAnswer
				break;
			case 'xuanze':
				postData.question_type = '选择'
				postData.question = '题目：' + customNewQues.value.problem + '，选项A：' + customNewQues.value.choice1 + '，选项B：' + customNewQues.value.choice2 + '，选项C：' + customNewQues.value.choice3 + '，选项D：' + customNewQues.value.choice4 + '，标准答案（为空则不知道）:' + customNewQues.value.answer
				postData.user_answer = customNewQues.value.stuAnswer
				break;
			case 'yuedu':
				postData.question_type = '阅读理解'
				postData.question += '阅读短文：' + customNewQues.value.content
				for(let xuanze of customNewQues.value.cuoTiList){
					postData.question += '，第' + Number(customNewQues.value.cuoTiList.indexOf(xuanze) + 1) + '题：' + xuanze.problem + '，选项A：' + xuanze.choice1 + '，选项B：' + xuanze.choice2 + '，选项C：' + xuanze.choice3 + '，选项D：' + xuanze.choice4 + '，标准答案（为空则不知道）:' + xuanze.answer
					postData.user_answer += xuanze.stuAnswer
				}
				break;
		}
		return postData
	}
	//暴露customNewQues给父组件
	const getCustomNewQues = ()=>{
		return customNewQues.value
	}
	defineExpose({
	      updateCustomNewQues,
		  getAiChatJson,
		  getCustomNewQues
	    });
	
	//题型
	const quesTypeColumns = ref([
		{
		  value: 'yuedu',
		  label: '阅读'
		},
		{
	      value: 'xuanze',
	      label: '选择'
	    },
	    {
	      value: 'fanyi',
	      label: '翻译'
	    },
		{
		  value: 'zuowen',
		  label: '作文'
		},
	])
	const selectCategory = ()=>{
		if(customNewQues.value.category === 'fanyi' || customNewQues.value.category === 'zuowen'){
			//阅读作文格式
			customNewQues.value = {
			  "stuID": customNewQues.value.stuID,
			  "category": customNewQues.value.category,
			  "field": customNewQues.value.field,
			  "answer": null,
			  "content": customNewQues.value.content,
			  "esID": customNewQues.value.esID,
			  "stuAnswer": null,
			  "falseReason": null,
			  "aiComment": null,
			  "cuoTiList": null,
			  "userComment": null
			}
		}else if(customNewQues.value.category === 'yuedu' || customNewQues.value.category === 'xuanze'){
			customNewQues.value = {
			  "stuID": customNewQues.value.stuID,
			  "category": customNewQues.value.category,
			  "field": customNewQues.value.field,
			  "content": customNewQues.value.content,
			  "esID": customNewQues.value.esID,
			  "cuoTiList": [],
			  "problem": null,
			  "answer": null,
			  "choice1": null,
			  "choice2": null,
			  "choice3": null,
			  "choice4": null,
			  "stuAnswer": null,
			  "aiComment": null,
			  "falseReason": null,
			}
		}
	}
	//OCR
	const ocrCommenSend = (type, position)=>{
		uni.chooseImage({
			sourceType: ['camera','album'],
		    success: (res) => {
		        console.log('选择的图片信息：', res.tempFilePaths[0]);
				uni.showLoading({
				    title: '分析中...'
				});
				uni.getStorage({
					key:'loginStorage',
					success(loginStorage) {
						console.log('token=' + loginStorage.data.token)
						let thisPostUrl = ''
						if(position === 1001 || position === 1002){
							thisPostUrl = globalProps.baseApi + 'photo/uploadForQuestion?type=' + type
						}else{
							thisPostUrl = globalProps.baseApi + 'photo/uploadForSearch'
						}
						// Ayden
						setTimeout(()=>{
							ocrCop(`In recent years, social media platforms have become an indispensable part of our life. For instance, social media played a crucial role in organizing protests and raising awareness about important social issues.
							However, the pervasive use of social media also brings about negative consequences. It can lead to the spread of misinformation, cyberbullying, and addiction, affecting individuals' mental health and well-being. 
							To mitigate the negative impacts of social media, fostering digital literacy and critical thinking skills is crucial. Emphasizing digital well-being and promoting meaningful interactions can maximize the benefits of social media while minimizing its drawbacks.`, position)
							uni.hideLoading();
						}, 5800)
						return
						uni.uploadFile({
						        url: 'http://www.fivecheers.com:1038/upload',
						        filePath: res.tempFilePaths[0],
						        name: 'file',
								header: {
								        'Authorization': 'Bearer ' + loginStorage.data.token
								},
						        success: (res) => {
									console.log('OCR识别返回res', res.data)
									ocrCop(res.data, position)
									uni.hideLoading();
						        },
						        fail: (err) => {
								  uni.hideLoading();
								  uni.showToast({
								      title: 'OCR识别失败',
								      icon: 'error'
								  });
						        }
						});
					}
				})
		    },
		    fail: (err) => {
		        console.error('调用相机失败：', err);
		    }
		});
	}
	const ocrCop = (data, position)=>{
		//1001 customNewQues.content
		//1002 customNewQues.stuAnswer
		//1003 customNewQues 选择
		//i customNewQues.cuoTiList[i]
		//打印结果填入相应位置
		switch(position){
			case 1001:
				customNewQues.value.content = data;
				break;
			case 1002:
				customNewQues.value.stuAnswer = data
				break;
			case 1003:
				customNewQues.value = JSON.parse(data)
				break;
			default:
				customNewQues.value.cuoTiList[position] = JSON.parse(data)
				/* const responseXuanze = JSON.parse(res)
				customNewQues.value.cuoTiList[position].choice1 = responseXuanze.choice1
				customNewQues.value.cuoTiList[position].choice2 = responseXuanze.choice2
				customNewQues.value.cuoTiList[position].choice3 = responseXuanze.choice3
				customNewQues.value.cuoTiList[position].choice4 = responseXuanze.choice4
				customNewQues.value.cuoTiList[position].stuAnswer = responseXuanze.stuAnswer
				customNewQues.value.cuoTiList[position].answer = responseXuanze.answer
				customNewQues.value.cuoTiList[position].problem = responseXuanze.problem */
				break;
		}
	}
	//AI分析
	const aiAnalysising = ref(false)
	let aiConversation = null
	const connectSocket = ()=>{
		if (!connected.value) {
			//连接ws
			aiConversation = socket.connectSocket({
				url: 'http://www.fivecheers.com:1020',
				success: function () {
					connected.value = true
				},
				fail: function () {
					connected.value = false
					// 连接失败后进行重连
					setTimeout(function () {
						connectSocket(); // 重连
					}, 3000);
				}
			});
			//连接成功
			aiConversation.onOpen(()=>{
				connected.value = true
				console.log('ai分析连接开启',aiConversation)
			})
			//连接关闭
			aiConversation.onClose(()=>{
				connected.value = false
				console.log('ai分析连接关闭',aiConversation)
			})
			//错误事件
			aiConversation.onError((e)=>{
				console.log('ai分析ws连接错误',e)
				connected.value = false
			})
			//收到消息
			aiConversation.onMessage((res)=>{
				if(res.data === '2580') return
				if(res.data === 'DONE') {
					aiAnalysising.value = false
					Vditor.preview(document.getElementById('ai-comment'), customNewQues.value.aiComment)
					return
				}
				customNewQues.value.aiComment += res.data
			})
		}
	
	}
	onMounted(()=>{
		connectSocket()
	})
	onBeforeUnmount(()=>{
		//关闭连接
		aiConversation.close()
	})
	//自动断线重连
	const connected = ref(false)
	watch(connected.value, (newValue, oldValue) => {
		if (!newValue) {
			console.log('连接断开，尝试重连');
			aiConversation = socket.connectSocket({
				url: 'ws://aiana.yym-free.com',
				complete() {}
			});
		}
	})
	
	//AI分析
	const aiAnalyseBtn = ()=>{
		aiAnalysising.value = true
		customNewQues.value.aiComment = ''
		let postTmp = getAiChatJson()
		const postFinal = JSON.stringify(postTmp)
		console.log('ai分析发送数据',postFinal)
		aiConversation.send({
			data: postFinal
		})
	}
	
	//上传题目
	const addNewQuesBtn = ()=>{
		const sendData = customNewQues.value
		console.log(sendData)
		uni.showLoading({
		    title: '添加中...'
		});
		uni.request({
		  url: globalProps.baseApi + 'cuotiji/addCuotiFromExe',
		  method: 'POST',
		  data: sendData,
		  success: function (res) {
			uni.hideLoading();
			uni.showToast({
				title: '添加成功',
				icon: 'success'
			})
			setTimeout(()=>{
				uni.switchTab({
					url: '/pages/HomePage/HomePage'
				})
			},1800)
		  },
		  fail: function (err) {
		    console.log('添加错题失败', err);
		    uni.showToast({
		    	title: '请求失败',
		    	icon: 'error'
		    })
		  }
		});
	}
	
	/**
	 * 阅读选择
	 */
	
	
</script>

<style>
	@import "@/css/global.css";
	@import "@/css/animation.css";
	
	.new-ques-container{
		height: 10px;
	}
	.ques-line{
		/* color: #222; */
		padding: 12px 4px;
		white-space: pre-line;
		word-break: break-all;
		display: flex;
		flex-direction: column;
	}
	.ques-line .btns-container{
		margin: 16px 0 8px;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.ques-line .btns-container button{
		padding: 4px 20px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 16px;
		margin: 0;
		color: #fff;
	}
	.ques-line .btns-container button:nth-child(2){
		background-color: #4d80f0;
	}
	.ques-line .btns-container button:nth-child(1){
		background-color: #aaaaaa;
	}
	.ques-line .text-area{
		width: calc(100% - 16px);
		min-height: 28px;
		height: auto;
		background-color: #ffffff55;
		padding: 8px;
		z-index: 0;
		white-space: pre-line;
		font-family: 'Courier New', Courier, monospace;
	}
	.h1{
		font-weight: bold;
		letter-spacing: 1px;
		font-size: 18px;
		margin-bottom: 12px;
	}
	.sure-btn-container{
		margin-bottom: 32px;
	}
	.sure-btn{
		margin: 12px 4px 24px 4px;
		width: calc(100% - 8px);
		display: flex;
		align-items: center;
		justify-content: center;
		height: 40px;
		background-color: #4d80f0;
		color: #fff;
		border-radius: 8px;
		box-shadow: 0 0 4px #00000022;
	}
	.ques-line-card{
		margin: 12px 0;
		padding: 12px;
		width: calc(100% - 26px);
		border-radius: 8px;
		border: 1px solid #4d80f0;
	}
	.h1-line{
		width: 100%;
		display: flex;
		align-items: center;
	}
	.picker-container{
		width: 110px;
		margin-bottom: 12px;
	}
	.h1-line :deep(.wd-picker__cell){
		background-color: #4d80f0cc !important; 
		border-radius: 8px;
	}
	.h1-line :deep(.wd-picker__value.false){
		color: #ffffff !important;
		font-size: 15px;
	}
	.h1-line :deep(.wd-picker__arrow){
		color: #ffffff !important;
	}
</style>