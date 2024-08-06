<template>
	<view class="galgame">
		<!-- 背景 -->
		<view class="galgame-bg">
			<!-- <image src="@/static/galbg.png" mode="aspectFill" class="galgame-bg-image"></image> -->
			<image :src="sceneInfo.sceneImageUrl" mode="aspectFill" class="galgame-bg-image"></image>
		</view>
		<!-- 返回 -->
		<view class="back" @click="navBack">
			<wd-icon name="thin-arrow-left" size="18px"></wd-icon>
		</view>
		<!-- 人物形象 -->
		<!-- <view class="partner">
			<image src="@/static/speechPartner.png" mode="aspectFit" class="partner-image"></image>
		</view> -->
		<!-- 当前对话框 -->
		<view class="current-message-wrapper">
			<view class="current-message">
				<!-- tts中显示messages队列顶部 -->
				<view v-if="TTSing">
					<view class="header">
						<view class="tag" style="background-color: rgb(152,0,0);">{{ sceneInfo.gptCharValue }}</view>
						<view class="tips">Tips: {{ currentTip }}</view>
					</view>
					<view class="content">{{ messages[messages.length - 1].content }}</view>
				</view>
				<!-- 未tts时显示语音识别当前的部分结果 -->
				<view v-else>
					<!-- 头部 -->
					<view class="header">
						<view class="tag" style="background-color: green;">你</view>
						<view class="tips">Tips: {{ currentTip }}</view>
					</view>
					<!-- 录音内容 -->
					<view class="recording-content">
						<view style="color: #ffffff;">
							<text>{{ title }}</text>
						</view>
						<view class="partial">
							<text>{{ partialResult }}</text>
						</view>
						<view class="volume" :style="{ width: valueWidth }"></view>
					</view>

				</view>
			</view>
		</view>

	</view>
	<AliyunTTS ref="ttsRef" @start-tts="startTTS" @end-tts="endTTS" />
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onUnmounted, watch } from 'vue'
import AliyunTTS from '@/components/AliyunTTS.vue'

// ws信息
const messages = ref([]) // 当前消息队列
const wsConnected = ref(false) // WebSocket是否已连接
const socketUrl = 'ws://8769.yym-free.com' // WebSocket地址
// const socketUrl = 'ws://192.168.51.190:8769' // WebSocket地址
const socket = ref(null) // WebSocket实例
const reconnectInterval = 3000 // 重连间隔
const responsing = ref(false) // GPT是否正在回应
const TTSing = ref(false)

// 语音信息
const constructingString = ref('') // 正在构建的字符串
const firstPlay = ref(true) // 是否第一次播放
const ttsRef = ref(null) // TTS实例

// 场景信息(从上一页传入, onMounted中获取)
const sceneInfo = ref({})

// 页面信息
const title = ref('未开始')
const text = ref('')
const partialResult = ref('...')
const result = ref('')
const valueWidth = ref('0px')

// 返回
const navBack = () => {
	uni.navigateBack()
}

// 识别启动回调：text赋值为空
const ontStart = () => {
	title.value = '...倾听中...'
	text.value = ''
	console.log('Event: start')
}

// 音量变化回调
const onVolumeChange = (e) => {
	valueWidth.value = 100 * e.volume + 'px'
	console.log('Event: volumeChange ' + valueWidth.value)
}

// 正在识别中回调：partialResult赋值为e.partialResult
const onRecognizing = (e) => {
	partialResult.value = e.partialResult
	console.log('Event: recognizing: ', e.partialResult)
}

// 识别完成回调：text += e.result，result赋值为text，partialResult赋值为e.result
const onRecognition = (e) => {
	text.value += e.result
	text.value ? (text.value += '\n') : (text.value = '')
	result.value = text.value
	partialResult.value = e.result
	console.log('Event: recognition:', e.result)
	// 识别一句话就发送
	addUsrMsg(e.result)
	endRecognize()
}

// 结束识别回调：text为空则提示没有识别到内容
const onEnd = () => {
	if (!text.value || text.value === '') {
		// plus.nativeUI.toast('没有识别到内容')
	}
	result.value = text.value
	title.value = '未开始'
	valueWidth.value = '0px'
	partialResult.value = '...'
	// addUsrMsg()
}

// 开始识别 方法
const startRecognize = () => {
	console.log('startRecognize')
	// #ifdef APP-PLUS
	plus.speech.startRecognize({
		engine: 'baidu',
		lang: 'en-us',
		'userInterface': false,
		'continue': true
	})
	// #endif
}

// 结束识别 方法
const endRecognize = () => {
	console.log('endRecognize')
	// #ifdef APP-PLUS
	plus.speech.stopRecognize()
	// #endif
}

// 连接WebSocket
const connectSocket = () => {
	console.log('connectSocket(), this.wsConnected:', wsConnected.value)
	if (!wsConnected.value) {
		socket.value = uni.connectSocket({
			url: socketUrl,
			success: function () {
				console.log('Socket连接成功')

			},
			fail: function () {
				console.error('Socket连接失败')
				wsConnected.value = false
				// 重连
				setTimeout(() => {
					connectSocket()
					setTimeout(() => {
						reconnectInitial()
					}, 2000)
				}, reconnectInterval)
			}
		})

		// 监听WebSocket打开事件
		socket.value.onOpen(function () {
			console.log("onopen: ", socket.value)
			console.log('Socket连接打开')
			// let scene = sceneToWsData()
			// console.log('发送场景信息:', scene)
			// wsConnected.value = true
			// // 连接成功后发送场景信息
			// socket.value.send({
			// 	data: scene
			// })
		})

		// 监听WebSocket关闭事件
		socket.value.onClose(function () {
			console.log('Socket连接关闭')
			wsConnected.value = false
			// 重连
			setTimeout(() => {
				connectSocket()
				setTimeout(() => {
					reconnectInitial()
				}, 2000)
			}, reconnectInterval)
		})

		// 监听WebSocket错误事件
		socket.value.onError(function (err) {
			console.error('Socket连接错误:', err)
			wsConnected.value = false
			// 重连
			setTimeout(() => {
				connectSocket()
				setTimeout(() => {
					reconnectInitial()
				}, 2000)
			}, reconnectInterval)
		})

		//收到ws信息
		socket.value.onMessage(function (res) {
			console.log('收到ws信息:', res.data)
			addAiMsg(res)
		})
	}
}


const currentTip = ref('这里将是给你的口语提示....')
// 添加AI消息
const addAiMsg = (res) => {
	let resData = JSON.parse(res.data)
	console.log('resData:', resData)
	if (resData.type === 'chat') {
		//发送后第一次收到正常回应
		if (!responsing.value) {
			messages.value.push({
				type: 'ai',
				content: resData.content
			})
			responsing.value = true
			return
		}

		//最后一次回应
		if (resData.content === 'None') {
			responsing.value = false
		} else {
			//过程中
			messages.value[messages.value.length - 1].content += resData.content
			// 句号切片
			if (
				resData.content != '。' &&
				resData.content != '：' &&
				resData.content != '，' &&
				resData.content != '！' &&
				resData.content != '？' &&
				resData.content != ',' &&
				resData.content != '!' &&
				resData.content != '?' &&
				resData.content != ':' &&
				resData.content != '.'
			) {
				constructingString.value += resData.content
			} else {
				constructingString.value += '。'
				ttsRef.value.addMsgToQueue(constructingString.value)
				constructingString.value = ''
				if (firstPlay.value) {
					ttsRef.value.playQueue()
					firstPlay.value = false
					console.log('this.firstPlay = false')
				}
			}
		}
	} else if (resData.type === 'tip') {
		currentTip.value = resData.content
	}
}

// 添加用户消息，正常的对话
const addUsrMsg = () => {
	if (text.value === '') return
	messages.value.push({
		type: 'usr',
		content: text.value
	})
	let sendPack = {
		scene: sceneInfo.value.sceneName,
		user_role: sceneInfo.value.myCharValue,
		gpt_role: sceneInfo.value.gptCharValue,
		main_line: sceneInfo.value.mainLine,
		msg: text.value,
		historyDialogue: messages.value
	}
	console.log('sendPack:', JSON.stringify(sendPack))
	socket.value.send({
		// data: text.value
		data: JSON.stringify(sendPack),
	})
	// text.value = ''

}

// 重连后发送的sendPack，包含历史对话
const reconnectInitial = () => {
	responsing.value = false
	if(messages.value[messages.value.length - 1].content === ''){
		messages.value.pop()
	}
	let sendPack = {
		scene: sceneInfo.value.sceneName,
		user_role: sceneInfo.value.myCharValue,
		gpt_role: sceneInfo.value.gptCharValue,
		main_line: sceneInfo.value.mainLine,
		msg: text.value,
		historyDialogue: messages.value
	}
	console.log('sendPack:', JSON.stringify(sendPack))
	socket.value.send({
		// data: text.value
		data: JSON.stringify(sendPack),
		// success: text.value = ''
	})

}

// 开始TTS时需要执行：
const startTTS = () => {
	console.log('AiConv开始TTS')
	TTSing.value = true
}

// 结束TTS时需要执行：
const endTTS = () => {
	console.log('AiConv结束TTS')
	firstPlay.value = true
	TTSing.value = false
	startRecognize()
}

// [Deprecated] 将场景信息转换为ws数据
const sceneToWsData = () => {
	return JSON.stringify({
		scene: sceneInfo.value.sceneName,
		user_role: sceneInfo.value.myCharValue,
		gpt_role: sceneInfo.value.gptCharValue,
		main_line: sceneInfo.value.mainLine
	})
}

onMounted(() => {
	// 接收场景信息
	sceneInfo.value = JSON.parse(uni.getStorageSync('sceneInfo'))
	console.log('sceneInfo:', sceneInfo.value)

	// 初始化
	messages.value = []

	// 连接WebSocket
	connectSocket()

	// 初始化TTS音色和语速
	ttsRef.value.setVoice('cally')
	ttsRef.value.setSpeed(50)

	// #ifdef APP-PLUS
	// 监听语音识别事件
	plus.speech.addEventListener('start', ontStart, false)
	plus.speech.addEventListener('volumeChange', onVolumeChange, false)
	plus.speech.addEventListener('recognizing', onRecognizing, false)
	plus.speech.addEventListener('recognition', onRecognition, false)
	plus.speech.addEventListener('end', onEnd, false)
	// #endif

	// #ifndef APP-PLUS
	uni.showToast({
		title: '暂不支持非APP端的语音识别',
		icon: 'error'
	})
	// #endif

	startRecognize()
})

onUnmounted(() => {
	socket.value.close()
	wsConnected.value = false
	endRecognize()
})

onBeforeUnmount(() => {
	console.log('onBeforeUnmount:', messages.value)
	socket.value.close()
	wsConnected.value = false
	let fake = [
		{
			type: 'usr',
			content: 'Hello, I want to practice my oral English.'
		},
		{
			type: 'ai',
			content: 'Hello, I am your AI teacher. I will help you practice oral English.'
		},
		{
			type: 'usr',
			content: 'Great! Let\'s start.'
		},
		{
			type: 'ai',
			content: 'OK. Please tell me about your favorite movie.'
		}
	]
	uni.$emit('backFromOralPractice', { msgList: messages.value })
	// uni.$emit('backFromOralPractice', { msgList: fake })
})

watch(wsConnected, (newVal) => {
	if (!newVal) {
		// 监听 WebSocket 关闭事件并进行重连
		setTimeout(() => {
			connectSocket()
			setTimeout(() => {
				reconnectInitial()
			}, 2000)
		}, reconnectInterval)
	}
})
</script>

<style>
@import "@/css/global.css";
@import "@/css/animation.css";

.back {
	position: fixed;
	top: calc(5px + var(--status-bar-height));
	left: 15px;
	z-index: 100;
	border-radius: 50%;
	background-color: rgba(255, 255, 255, 1);
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	width: 30px;
	height: 30px;
	display: flex;
	justify-content: center;
	align-items: center;
}

.galgame {
	position: relative;
	width: 100%;
	height: 100%;
}

.galgame-bg {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;
}

.galgame-bg-image {
	width: 100%;
	height: 100%;
}

/* .partner {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;

}

.partner-image {
	position: fixed;
	bottom: 0;
	right: 0;
	height: 60vh;
} */

.current-message-bg {}


.current-message-wrapper {
	z-index: 100;
	background-color: rgba(0, 0, 0, 0.6);
	position: fixed;
	bottom: 0;
	left: 0;
	padding: 20px;
	z-index: 100;
	width: calc(100% - 40px);
	height: 30%;
}

.current-message {
	box-sizing: border-box;
	color: white;
	font-size: 14px;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding-bottom: 10px;
	border-bottom: 1px solid rgba(255, 255, 255, 0.4);
}

.content{
	margin-top: 15px;
}

.tag {
	width: fit-content;
	box-sizing: content-box;
	border-radius: 10px;
	padding: 2px 8px;
	font-size: 20px;
	font-weight: bold;
}

.tips {
	max-width: 70%;
}

.recording-content {
	margin-top: 15px;
	display: flex;
	flex-direction: column;
	/* align-items: center; */
}

.volume {
	align-self: center;
}





.partial {
	/* width: 100%; */
	height: 40px;
	margin-top: 16px;
	font-size: 12px;
	color: #FFFFFF;
}

.volume {
	width: 10px;
	height: 6px;
	border-style: solid;
	display: inline-block;
	box-sizing: border-box;
	border-width: 1px;
	border-color: #CCCCCC;
	border-radius: 50%;
	background-color: #00CC00;
}
</style>