<template>
	<div class="com-container">
		<!--对话-->
		<scroll-view @scroll="scrollHandler" @scrolltolower="setAtBottom" ref="scrollContainer" scroll-y="true"
			:scroll-top="scrollTop" class="message-container">
			<!-- <div class="message-self" v-for="item in messages">
				
				<div v-if="item.type==='ai'" class="ai-head">
					<wd-icon name="chat" color="#fff" size="22px"></wd-icon>
				</div>
				<div v-if="item.type==='ai'" class="ai-message">
					{{ item.content }}
				</div>
				<div style="flex: 1;">
					
				</div>
				
				<div v-if="item.type === 'usr'" class="usr-message">
					{{ item.content }}
				</div>
				<div v-if="item.type === 'usr'" class="usr-head">
					<wd-icon name="user-circle" color="#fff" size="22px"></wd-icon>
				</div>
			</div> -->

			<div class="message-self" v-for="item in messages">
				<!--ai-->
				<div v-if="item.type === 'ai'" class="ai-head">
					<wd-icon name="chat" color="#fff" size="22px"></wd-icon>
				</div>
				<div v-if="item.type === 'ai'" class="ai-message">
					{{ isRef(item.content) ? item.content.value : item.content }}
					<view style="margin-top: 10rpx; z-index: 99999">
						<!-- 新增按钮：智能巩固 -->
						<button v-if="item.msgShowConsoliButton" size="default" @click="getAllRedoThenJump"
							style="backgroundColor:#4d80f0; color:#ffffff">去做题</button>
						<!-- 新增按钮：智能推荐 -->
						<button v-if="item.msgShowRecommend" size="default" @click="jumpToRecommend"
							style="backgroundColor:#4d80f0; color:#ffffff">推荐习题</button>
						<!-- 新增按钮：学情分析 -->
						<button v-if="item.msgShowAnalysis" size="default" @click="jumpToAnalysis"
							style="backgroundColor:#4d80f0; color:#ffffff">学情分析</button>
					</view>
				</div>
				<div style="flex: 1;"></div>
				<!--用户-->
				<div v-if="item.type === 'usr' && item.content.charAt(0) !== '$'" class="usr-message">
					{{ item.content }}
				</div>
				<div v-if="item.type === 'usr' && item.content.charAt(0) !== '$'" class="usr-head">
					<wd-icon name="user-circle" color="#fff" size="22px"></wd-icon>
				</div>
			</div>

		</scroll-view>

		<!-- 样例prompt -->
		<view class="example-prompt" v-if="promptShow">
			<view class="component" @click="promptClick(1)">
				<view class="example-title">{{ prompt1 }}</view>
				<view class="example-self">{{ prompt1Text }}</view>
			</view>
			<view class="component" @click="promptClick(2)">
				<view class="example-title">{{ prompt2 }}</view>
				<view class="example-self">{{ prompt2Text }}</view>
			</view>
			<view class="component" @click="promptClick(3)">
				<view class="example-title">{{ prompt3 }}</view>
				<view class="example-self">{{ prompt3Text }}</view>
			</view>
			<view class="component" @click="promptClick(4)">
				<view class="example-title">{{ prompt4 }}</view>
				<view class="example-self">{{ prompt4Text }}</view>
			</view>
		</view>

		<!--输入-->
		<div class="input-container" v-if="!isOralPractice">
			<textarea placeholder="请输入问题" maxlength="-1" class="input-inner" v-model="textSubmit" auto-height />
			<div class="btn" v-if="!showLoading && connected" @click="submitButtonClick">
				<wd-icon name="chat" color="#fff" size="22px"></wd-icon>
			</div>
			<div class="btn" v-else>
				<wd-loading type="outline" size="22px" color="#4d80f0" />
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, defineProps, defineEmits, isRef, onMounted } from 'vue';
import { chatRouterPages, chatRouterTabs, tabsLinks } from '@/js/chatRouter.js'
import { globalProps } from '../js/global';
import { onLoad, onUnload, onHide, onShow } from '@dcloudio/uni-app';

// 给用户预制的4个prompt是否显示
const promptShow = ref(false)
const prompt1 = ref('问候')
const prompt1Text = ref('老师好，请问您能如何帮助我学习英语？')
const prompt2 = ref('题目巩固')
const prompt2Text = ref('我想巩固下之前提的问题')
const prompt3 = ref('学情分析')
const prompt3Text = ref('请您分析下我最近的学习情况')
const prompt4 = ref('习题推荐')
const prompt4Text = ref('请根据我的学习情况给我推荐一些习题')

const promptClick = (index) => {
	promptShow.value = false
	switch (index) {
		case 1:
			textSubmit.value = prompt1Text.value
			submitButtonClick()
			break
		case 2:
			// textSubmit.value = prompt2Text.value
			addNewMsg('mode2', prompt2Text.value)
			showConsoliButton.value = true
			showLoading.value = true
			break
		case 3:
			// textSubmit.value = prompt3Text.value
			addNewMsg('mode3', prompt3Text.value)
			showAnalysis.value = true
			showLoading.value = true
			break
		case 4:
			// textSubmit.value = prompt4Text.value
			addNewMsg('mode1', prompt4Text.value)
			showRecommend.value = true
			showLoading.value = true
			break
	}
	// setTimeout(() => {
	// 	submitButtonClick()
	// 	promptShow.value = false
	// }, 200)
}

onHide(() => {
	isShow.value = false
	uni.closeSocket({
		success() {
			console.log('首页ws已断开')
		}
	})
})

// 页面是否展示
const isShow = ref(true)
// ws是否连接
const connected = ref(false)


// WebSocket连接部分

// let socketUrl = 'ws://aitalk.yym-free.com?userId=' + globalProps.userInfo.id;
let socketUrl = 'ws://www.fivecheers.com:1021?userId=' + globalProps.userInfo.id;
// let socketUrl = 'ws://192.168.149.190:8765';

let socket = null;
let reconnectInterval = 3000;

function connectSocket() {
	if (isShow.value && !connected.value) {
		socket = uni.connectSocket({
			url: socketUrl,
			success: function () {
				console.log('Socket连接成功');
				connected.value = true
			},
			fail: function () {
				console.error('Socket连接失败');
				connected.value = false
				// 连接失败后进行重连
				setTimeout(function () {
					connectSocket(); // 重连
				}, reconnectInterval);
			}
		});

		// 监听WebSocket关闭事件
		socket.onClose(function () {
			console.log('Socket连接关闭');
			connected.value = false
			responsing.value = false
			showLoading.value = false
			// 连接关闭后进行重连
			setTimeout(function () {
				connectSocket(); // 重连
			}, reconnectInterval);
		});

		// 监听WebSocket错误事件
		socket.onError(function (err) {
			console.error('Socket连接错误:', err);
			connected.value = false
			// 连接错误后进行重连
			setTimeout(function () {
				connectSocket(); // 重连
			}, reconnectInterval);
		});

		//收到ws信息
		socket.onMessage(function (res) {
			if (isShow.value) {
				if (res.data === '3690') return
				addAiMsg(res)
			}
		});
	}

}

onMounted(() => {
	if (props.homepagePrompt) {
		promptShow.value = true
	}
})
onShow(() => {
	setTimeout(() => {
		isShow.value = true
		responsing.value = false

		connectSocket()

		// 添加监听
		if (props.isOralPractice) {
			uni.$on('backFromOralPractice', function (data) {
				console.log('监听到事件来自 backFromOralPractice', data);
				setMessages(data.msgList)
			})
		}
	}, 200)
})


const props = defineProps({
	quesId: Number,
	homepagePrompt: {
		type: Boolean,
		default: false
	},
	isOralPractice: {
		type: Boolean,
		default: false
	}
})


const emit = defineEmits(['readReply', 'onlyRead', 'onlyStop'])
const textSubmit = ref('')
const aiMessageContent = ref('');
const responsing = ref(false)

//scroll-div scroll bottom
const scrollTop = ref(0)
const atBottom = ref(true)
const setAtBottom = () => {
	atBottom.value = true
}
const scrollHandler = (scroll) => {
	if (scroll.detail.scrollTop < scrollTop.value) {
		atBottom.value = false
	}
}
const scrollToBottom = () => {
	if (atBottom.value) {
		setTimeout(() => {
			scrollTop.value += 20
			atBottom.value = true
		}, 200)
	}
}

const quesContent = ref('')
const replaying = ref(true)
const messages = ref([])


// 提供一个直接给messages赋值的方法:
const setMessages = (newMessages) => {
	messages.value = newMessages
}

// 提供一个直接给messages添加一条消息的方法:
const pushMessage = (newMessage) => {
	messages.value.push(newMessage)
}

// messages去ref如果需要传给后端
// const convertMessagesToPlain = () => {
// 	return messages.value.map(msg => {
// 		const { type, content } = msg;
// 		return {
// 			type,
// 			content: isRef(content) ? content.value : content
// 		}
// 	})
// }


//增加用户消息
const addUsrMsg = () => {
	socket.send({
		data: textSubmit.value
	});
	messages.value.push({
		type: 'usr',
		content: textSubmit.value
	})
	textSubmit.value = ''
	scrollToBottom()
}

const addNewMsg = (mode, content) => {
	socket.send({
		data: mode
	});
	messages.value.push({
		type: 'usr',
		content: content
	})
	textSubmit.value = ''
	scrollToBottom()
}

const waitingForJump = ref(false)
const showLoading = ref(false)

// 接收7410信息
const showConsoliButton = ref(false)

// 接收2580智能推荐消息
const showRecommend = ref(false)

// 接收1234学情分析
const showAnalysis = ref(false)

//增加ai消息
const addAiMsg = (res) => {
	// April 14th 新增逻辑：显示按钮
	if (!responsing.value) {
		// 判断第一次接收的消息是否为"7410"，如果是则显示按钮
		if (res.data === '7410') {
			console.log('收到7410')
			messages.value.push({
				type: 'ai',
				content: '',
				msgShowConsoliButton: false,
				msgShowRecommend: false,
				msgShowAnalysis: false
			})
			showConsoliButton.value = true
			responsing.value = true
			// 向父页面发送事件，开始读
			// emit('onlyRead')
			return
		} else if (res.data === '2580') {
			// 判断第一次接收的消息是否为2580智能推荐
			console.log('收到2580')
			messages.value.push({
				type: 'ai',
				content: '',
				msgShowConsoliButton: false,
				msgShowRecommend: false,
				msgShowAnalysis: false
			})
			showRecommend.value = true
			responsing.value = true
			// 向父页面发送事件，开始读
			// emit('onlyRead')
			return
		} else if (res.data === '1234') {
			console.log('收到1234')
			messages.value.push({
				type: 'ai',
				content: '',
				msgShowConsoliButton: false,
				msgShowRecommend: false,
				msgShowAnalysis: false
			})
			showAnalysis.value = true
			responsing.value = true
			// 向父页面发送事件，开始读
			// emit('onlyRead')
			return
		} else {
			messages.value.push({
				type: 'ai',
				content: res.data
			})
			responsing.value = true
			uni.$emit('firstGetMessage', res.data)
			return
		}
	}


	//最后一次回应
	if (res.data === 'DONE') {
		responsing.value = false
		// emit('onlyStop')
		showLoading.value = false
		// 如果7410，则显示按钮
		if (showConsoliButton.value) { // 这几个需要修改到点击按钮时触发，而不是根据第一个消息code
			messages.value[messages.value.length - 1].msgShowConsoliButton = true;
			showConsoliButton.value = false 
		}
		// 如果2580，则显示按钮
		if (showRecommend.value) { // 这几个需要修改到点击按钮时触发，而不是根据第一个消息code
			messages.value[messages.value.length - 1].msgShowRecommend = true;
			showRecommend.value = false
		}
		// 如果1234，则显示按钮
		if (showAnalysis.value) { // 这几个需要修改到点击按钮时触发，而不是根据第一个消息code
			messages.value[messages.value.length - 1].msgShowAnalysis = true;
			showAnalysis.value = false
		}
	}
	else {
		//过程中
		messages.value[messages.value.length - 1].content += res.data
		uni.$emit('continueGetMsg', res.data)
	}
	scrollToBottom()
}


// 跳转学情分析
const jumpToAnalysis = () => {
	console.log('跳转学情分析')
	uni.navigateTo({
		url: '/pages/GrowPage/GrowPage'
	})
}

// 跳转到推荐习题页面
const jumpToRecommend = () => {
	console.log('跳转到推荐习题页面')
	uni.navigateTo({
		url: '/pages/RecommandPage/RecommandPage'
	})
}

// 获取所有错题并跳转到遗忘曲线页面
const getAllRedoThenJump = () => {
	console.log('获取所有错题并跳转到遗忘曲线页面')
	let getUrl = globalProps.baseApi + 'cuotiji/cuotiForRedo/?userID=' + globalProps.userInfo.id
	uni.request({
		url: getUrl,
		method: 'GET',
		success: (res) => {
			console.log('成功生成练习：', res.data)
			uni.setStorageSync('exerciseList', res.data);
			allRedoJump()
		},
		fail: (err) => {
			uni.showToast({
				title: '生成练习失败',
				icon: 'none'
			})
			console.log(err)
		}
	})

}

// 跳转到遗忘曲线页面
const allRedoJump = () => {
	uni.navigateTo({
		url: '/pages/ReviewPage/ReviewDetail/ReviewDetail',
		// 将题目数组作为参数传递给ExerciseDetailPage页面
		success: (res) => {
			console.log('跳转成功', res);
			if (res.errMsg === 'navigateTo:ok') {
				// 传递参数
				// uni.setStorageSync('exerciseList', this.exerciseList);
			}
		}
	});
}
const submitButtonClick = () => {
	if (textSubmit.value) {
		showLoading.value = true
		promptShow.value = false
		addUsrMsg()
	}
	/*
	let aiContent;
	if (textSubmit.value) {
		messages.value.push({
			type: 'usr',
			content: textSubmit.value
		})
	
		const command = textSubmit.value.toLowerCase().trim();
	
		// 查找命令是否在chatRouterPages中
		const pageRoute = chatRouterPages[command];
		if (pageRoute) {
			// 如果找到对应的路由，使用uni.navigateTo跳转到该页面
			aiContent = '中嘞哥，已为您跳转到' + pageRoute + '页面';
			// getAudioUrl(aiContent);
			emit('readReply', aiContent)
			messages.value.push({
				type: 'ai',
				content: aiContent
			})
			uni.navigateTo({
				url: pageRoute
			});
		} else {
			// 查找命令是否在chatRouterTabs中
			const tabRoute = chatRouterTabs[command];
			if (tabRoute) {
				// 如果找到对应的tab，使用uni.switchTab跳转到该tab页面
				aiContent = '中嘞哥，已为您切换到' + tabRoute + '页面';
				// getAudioUrl(aiContent); // 更改为触发事件
				emit('readReply', aiContent)
				messages.value.push({
					type: 'ai',
					content: aiContent
				})
				uni.switchTab({
					url: tabRoute
				});
			} else {
				console.log("submit text: " + textSubmit.value);
				// 暂时读用户输入的文本，有待改成从后端获取gpt返回的文本消息
				// getAudioUrl(textSubmit.value); // 更改为触发事件
				emit('readReply', textSubmit.value)
				// messages.value.push({
				// 	type: 'ai',
				// 	content: 'gpt返回的文本消息'
				// })
				const newAiMessage = {
					type: 'ai',
					content: ref('')
				}
				messages.value.push(newAiMessage);
	
				let index = 0;
				const textReceiveFromGpt = 'gpt返回的文本消息gpt返回的文本消息gpt返回的文本消息gpt返回的文本消息gpt返回的文本消息gpt返回的文本消息';
				const addCharWithDelay = () => {
					if (index < textReceiveFromGpt.length) {
						newAiMessage.content.value += textReceiveFromGpt[index];
						index++;
						// 生成0到200毫秒之间的随机数作为延时时间
						const randomDelay = Math.random() * 200;
						setTimeout(addCharWithDelay, randomDelay);
					}
				}
	
				addCharWithDelay();
			}
		}
		textSubmit.value = ''; 
	} */
}
</script>

<script>
//参考
//建立websocket
/* const ws = ref('')
const startWebSocket=()=>{
  try {
	ws.value = new WebSocket(websocketUrl+userId.value);
	ws.value.onmessage = getMessage
	ws.value.onerror = onError
  }catch (e){
	message.error('与服务器建立websocket对话失败，'+e)
  }
}
const onError = ()=>{
  message.error('websocket连接出错，请重新选择对话')
}
//收到消息
const getMessage = (msg)=>{
  var messageDetail = JSON.parse(msg.data)
  messageDetail.sendTime = timeCorrect(messageDetail.sendTime)
  allMessages.value.push(messageDetail)
	
  nextTick(()=>{
	scrollContainer.value.scrollTo({
	  top: scrollContainer.value.scrollHeight,
	  behavior: 'smooth',
	});
  })
}
//发送消息
const sendMessage = ()=>{
  if (ws.value && ws.value.readyState === WebSocket.OPEN){
	try {
	  ws.value.send(JSON.stringify({
		messageId: dialogueId.value,
		toUserId: otherId.value,
		messageContent: inputText.value,
		messageImg: fileUrl.value
	  }))
	  inputText.value = ''
	  fileList.value = []
	  fileUrl.value = ''
	}catch (e){
	  message.error('发送失败，'+e)
	}
  }else{
	message.error('发送失败，请先选择会话')
  }
}
	
onUnmounted(()=>{
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
	ws.value.close();
  }
}) */
</script>

<style>
@import url("@/css/global.css");
@import url("@/css/animation.css");

.com-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	height: 100%;
}

/*对话*/
.message-container {
	flex: 1;
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: start;
	overflow-y: scroll;
	overflow-x: hidden;
}

.message-self {
	width: 100%;
	height: auto;
	margin-bottom: 8px;
	display: flex;
	align-items: flex-start;
	justify-content: space-around;
}

.message-self .ai-head {
	width: 36px;
	height: 36px;
	background-color: #4942ad;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.message-self .ai-message {
	max-width: calc(100% - 92px);
	margin: 4px 8px;
	color: #fff;
	background-color: rgba(255, 255, 255, 0.7);
	/* 阴影 */
	box-shadow: 0px 0px 8px -2px rgba(0, 0, 0, 0.1);
	color: #333;
	padding: 8px;
	border-top-right-radius: 8px;
	border-bottom-right-radius: 8px;
	border-bottom-left-radius: 8px;
	letter-spacing: 1px;
	white-space: pre-line;
}

.message-self .usr-message {
	max-width: calc(100% - 92px);
	margin: 4px 8px;
	color: #fff;
	background-color: #4942ad;
	box-shadow: 0px 0px 8px -2px rgba(0, 0, 0, 0.1);
	padding: 8px;
	border-top-left-radius: 8px;
	border-bottom-right-radius: 8px;
	border-bottom-left-radius: 8px;
	letter-spacing: 1px;
	white-space: pre-line;
}

.message-self .usr-head {
	width: 36px;
	height: 36px;
	background-color: #4942ad;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
}

/*输入*/
.input-container {
	max-height: 80px;
	width: 100%;
	display: flex;
	align-items: flex-end;
	justify-content: space-between;
	position: relative;
}

.input-container .input-inner {
	color: black;
	background-color: #fdfdfd;
	border: 1px solid #4d80f044;
	max-height: 60px;
	height: auto;
	min-height: 24px;
	padding: 8px 8px 4px 8px;
	width: calc(100% - 76px);
	margin-top: 16px;
	border-radius: 4px;
}

.input-container .btn {
	width: 48px;
	height: 36px;
	background-color: #4942ad;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
}


/* 底部 */
.example-prompt {
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	animation: bottom-in-ani .8s 1;
}

.component {
	background: linear-gradient(90deg, rgba(48,26,133,1) 0%, rgba(74, 30, 105, 1.0) 100%);
	box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.1);
	width: calc(100%);
	margin: 10px 0 0 0;
	padding: 10px;
	border-radius: 10px;
}

.example-title {
	/* font-size: 18px; */
	font-weight: bold;
	margin-bottom: 5px;
}

.example-self {
	font-size: small;
	color: #aaa;
}
</style>