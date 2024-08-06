<template>
	<view class="tabbarpage-container">
		<view class="status_bar">
			<!-- 这里是状态栏 -->
		</view>
		<view class="page-header-back">
			<navigator open-type="navigateBack" hover-class="navigator-hover">
				<view class="back-icon">
					<wd-icon name="thin-arrow-left" size="18px"></wd-icon>
				</view>
			</navigator>
			<view class="title">
				口语教练
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>
		</view>

		<view class="tabbarpage-body content">
			<textarea class="result" placeholder="语音识别内容" :value="result"></textarea>
			<view class="recogniz">
				<view style="color: #0000CC;">
					<text>{{ title }}</text>
				</view>
				<view class="partial">
					<text>{{ partialResult }}</text>
				</view>
				<view class="volume" :style="{ width: valueWidth }"></view>
			</view>
			<button type="default" @touchstart="startRecognize" @touchend="endRecognize">按下开始&amp;松开结束</button>
			<button type="default" @click="startRecognize">点击开始</button>
			<button type="default" @click="endRecognize">点击结束</button>
			
		</view>
		<AliyunTTS ref="ttsRef" @start-tts="startTTS" @end-tts="endTTS" />
	</view>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onUnmounted, watch } from 'vue'
import AliyunTTS from '@/components/AliyunTTS.vue'
// import { onHide } from '@dcloudio/uni-app'

// ws信息
const messages = ref([]) // 当前消息队列
const wsConnected = ref(false) // WebSocket是否已连接
const socketUrl = 'ws://oral.yym-free.com' // WebSocket地址
const socket = ref(null) // WebSocket实例
const reconnectInterval = 3000 // 重连间隔
const responsing = ref(false) // GPT是否正在回应

// 语音信息
const constructingString = ref('') // 正在构建的字符串
const firstPlay = ref(true) // 是否第一次播放
const ttsRef = ref(null) // TTS实例


// 页面信息
const title = ref('未开始')
const text = ref('')
const partialResult = ref('...')
const result = ref('')
const valueWidth = ref('0px')

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
		plus.nativeUI.toast('没有识别到内容')
	}
	result.value = text.value
	title.value = '未开始'
	valueWidth.value = '0px'
	partialResult.value = '...'
	addUsrMsg()
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
				wsConnected.value = true
			},
			fail: function () {
				console.error('Socket连接失败')
				wsConnected.value = false
				// 连接失败后进行重连
				setTimeout(function () {
					connectSocket() // 重连
				}, reconnectInterval)
			}
		})

		// 监听WebSocket关闭事件
		socket.value.onClose(function () {
			console.log('Socket连接关闭')
			wsConnected.value = false
			// 连接关闭后进行重连
			setTimeout(function () {
				connectSocket() // 重连
			}, reconnectInterval)
		})

		// 监听WebSocket错误事件
		socket.value.onError(function (err) {
			console.error('Socket连接错误:', err)
			wsConnected.value = false
			// 连接错误后进行重连
			setTimeout(function () {
				connectSocket() // 重连
			}, reconnectInterval)
		})

		//收到ws信息
		socket.value.onMessage(function (res) {
			console.log('收到ws信息:', res.data)
			addAiMsg(res)
		})
	}
}

// 添加AI消息
const addAiMsg = (res) => {
	//发送后第一次收到正常回应
	if (!responsing.value) {
		messages.value.push({
			type: 'ai',
			content: res.data
		})
		responsing.value = true
		return
	}

	//最后一次回应
	if (res.data === 'None') {
		responsing.value = false
	} else {
		//过程中
		messages.value[messages.value.length - 1].content += res.data
		// 句号切片
		if (
			res.data != '。' &&
			res.data != '：' &&
			res.data != '，' &&
			res.data != '！' &&
			res.data != '？' &&
			res.data != ',' &&
			res.data != '!' &&
			res.data != '?' &&
			res.data != ':' &&
			res.data != '.'
		) {
			constructingString.value += res.data
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
}

// 添加用户消息
const addUsrMsg = () => {
	if (text.value === '') return
	messages.value.push({
		type: 'usr',
		content: text.value
	})
	socket.value.send({
		data: text.value
	})
	text.value = ''
}

// 开始TTS时需要执行：
const startTTS = () => {
	console.log('AiConv开始TTS')
}

// 结束TTS时需要执行：
const endTTS = () => {
	console.log('AiConv结束TTS')
	firstPlay.value = true
	startRecognize()
}

onMounted(() => {
	messages.value = []
	connectSocket()
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
})

onUnmounted(() => {
	socket.value.close()
	wsConnected.value = false
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
		}, reconnectInterval)
	}
})
</script>

<style>
@import "@/css/global.css";
@import "@/css/animation.css";

.content {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}

.recogniz {
	width: 200px;
	height: 100px;
	padding: 12px;
	margin: 50px auto;
	background-color: rgba(0, 0, 0, 0.5);
	border-radius: 16px;
	text-align: center;
}

.partial {
	width: 100%;
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

.result {
	color: #CCCCCC;
	border: #00CCCC 1px solid;
	margin: 25px auto;
	padding: 6px;
	width: 80%;
	height: 100px;
}
</style>