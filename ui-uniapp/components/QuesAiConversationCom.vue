<template>
	<div class="com-container">
		<!--AI头部-->
		<AiCharacterCom :enableHide="true" class="ai-head-container"></AiCharacterCom>
		<!--对话-->
		<scroll-view @scroll="scrollHandler" @scrolltolower="setAtBottom" ref="scrollContainer" scroll-y="true" :scroll-top="scrollTop" class="message-container">
			<div class="message-self" v-for="item in messages">
				<!--ai-->
				<div v-if="item.type === 'ai'" class="ai-head">
					<wd-icon name="chat" color="#fff" size="22px"></wd-icon>
				</div>
				<div v-if="item.type === 'ai'" class="ai-message">
					{{ item.content }}
				</div>
				<div style="flex: 1;"></div>
				<!--用户-->
				<div v-if="item.type === 'usr'" class="usr-message">
					{{ item.content }}
				</div>
				<div v-if="item.type === 'usr'" class="usr-head">
					<wd-icon name="user-circle" color="#fff" size="22px"></wd-icon>
				</div>
			</div>
		</scroll-view>
		<!--输入-->
		<div class="input-container">
			<textarea placeholder="请输入问题" maxlength="-1" class="input-inner" v-model="textSubmit" auto-height />
			<div class="btn" v-if="!showLoading && connected && conversationQues !== null" @click="submitButtonClick">
				<wd-icon name="chat" color="#fff" size="22px"></wd-icon>
			</div>
			<div class="btn" v-else>
				<wd-loading type="outline" size="22px" color="#4942ad" />
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, defineProps, defineEmits, isRef, onMounted, onBeforeUnmount, watch, defineExpose } from 'vue';
	import { chatRouterPages, chatRouterTabs, tabsLinks } from '@/js/chatRouter.js'
	import { globalProps } from '../js/global';
	import { onLoad, onUnload, onHide } from '@dcloudio/uni-app'
	import socket from 'plus-websocket'
	import AiCharacterCom from '@/components/AiCharacterCom.vue'
	
	/**
	 * 对话
	 */
	//获取当前对话对应的问题
	const conversationQues = ref(null)
	onLoad(()=>{
		uni.$on('updateConversationQues',(e)=>{
			conversationQues.value = e
		})
	})
	
	//向父组件暴露对话数组
	const getDialogues = ()=>{
		let dialogToSend = JSON.parse(JSON.stringify(messages.value))
		for (let message of dialogToSend) {
			message.userType = message.type
			message.dialogContent = message.content
		}
		return dialogToSend
	}
	const setDialogs = (newDialogs)=>{
		for (let dialog of newDialogs) {
			dialog.type = dialog.userType
			dialog.content = dialog.dialogContent
		}
		console.log('获取到历史记录对话',newDialogs)
		messages.value = newDialogs
	}
	//滚动到底部
	const scrollToBottomExpose = ()=>{
		scrollTop.value += 50000
	}
	defineExpose({
		getDialogues,
		setDialogs,
		scrollToBottomExpose
	})
	
	const {conversationType} = defineProps({
		conversationType: Number
	})
	
	const handleConversationType = ()=>{
		switch(conversationType){
			case 0:
				//新问题
				messages.value.push({
					type: 'ai',
					content: '您好，欢迎您向我提出新问题。您可以在页面底部识别上传英语题目，我将围绕您的问题帮助您学习。'
				})
				break;
			
		}
	}
	
	//终版ws连接
	let aiConversation = null
	const connectSocket = ()=>{
		if (!connected.value) {
			//连接ws
			aiConversation = socket.connectSocket({
				url: 'ws://www.fivecheers.com:1026',
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
				console.log('问题ai对话连接开启',aiConversation)
			})
			//连接关闭
			aiConversation.onClose(()=>{
				connected.value = false
				console.log('问题ai对话关闭',aiConversation)
				responsing.value = false
				showLoading.value = false
			})
			//错误事件
			aiConversation.onError((e)=>{
				console.log('问题ai对话ws连接错误',e)
				connected.value = false
			})
			//收到消息
			aiConversation.onMessage((res)=>{
				if(res.data === '2580') return
				addAiMsg(res)
			})
		}
	
	}
	onMounted(()=>{
		handleConversationType()
		connectSocket()
	})
	
	onBeforeUnmount(()=>{
		//关闭连接
		aiConversation.close()
		//关闭获取问题
		uni.$off('updateConversationQues')
	})
	//自动断线重连
	const connected = ref(false)
	watch(connected.value, (newValue, oldValue) => {
		if (!newValue) {
			console.log('连接断开，尝试重连');
			setTimeout(()=>{
				connectSocket()
			},3000)
		}
	})

	const showLoading = ref(false)
	const textSubmit = ref('')
	const aiMessageContent = ref('');
	const responsing = ref(false)
	const scrollContainer = ref()
	//滚动到底部
	const scrollTop = ref(0)
	const atBottom = ref(true)
	const setAtBottom = ()=>{
		atBottom.value = true
	}
	const scrollHandler = (scroll)=>{
		if(scroll.detail.scrollTop < scrollTop.value ){
			atBottom.value = false
		}
	}
	const scrollToBottom = ()=>{
		if(atBottom.value){
			setTimeout(()=>{
				scrollTop.value += 20
				atBottom.value = true
			},200)
		}
	}
	const quesContent = ref('')
	const messages = ref([])
	
	//增加用户消息
	const addUsrMsg = ()=>{
		let dataToSend = JSON.parse(JSON.stringify(conversationQues.value))
		dataToSend.msg = textSubmit.value
		dataToSend.historyDialogue = JSON.parse(JSON.stringify(messages.value))
		if(dataToSend.historyDialogue.length <=1 ){
			dataToSend.historyDialogue = []
		}
		console.log('问题对话发送数据', JSON.stringify(dataToSend))
		aiConversation.send({
		  data: JSON.stringify(dataToSend)
		});
		messages.value.push({
			type: 'usr',
			content: textSubmit.value
		})
		textSubmit.value = ''
		scrollToBottom()
	}


	//增加ai消息
	const addAiMsg = (res)=>{
		//发送后第一次收到回应
		if(!responsing.value){
			if (res.data === 'DONE') return
			messages.value.push({
				type: 'ai',
				content: res.data
			})
			responsing.value = true
			uni.$emit('firstGetMessage', res.data)
			return
		}
		//最后一次回应
		if(res.data === 'DONE'){
			responsing.value = false
			showLoading.value = false
		}
		else{
			//过程中
			messages.value[messages.value.length - 1].content +=res.data
			uni.$emit('continueGetMsg', res.data)
		}
		scrollToBottom()
	}
	
	
	const submitButtonClick = () => {
		if (textSubmit.value) {
			showLoading.value = true
			addUsrMsg()
		}
	
}
</script>


<style>
	.com-container{
		display: flex;
		flex-direction: column;
		align-items: center;
		height: 100%;
	}
	/*对话*/
	.message-container{
		flex: 1;
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: start;
		overflow-y: scroll;
		overflow-x: hidden;
	}
	.message-self{
		width: 100%;
		height: auto;
		margin-bottom: 8px;
		display: flex;
		align-items: flex-start;
		justify-content: space-around;
	}
	.message-self .ai-head{
		width: 36px;
		height: 36px;
		background-color: #4942ad;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.message-self .ai-message{
		max-width: calc(100% - 92px);
		margin: 4px 8px;
		color: #fff;
		background-color: #fff;
		color: #333;
		padding: 8px;
		border-top-right-radius: 8px;
		border-bottom-right-radius: 8px;
		border-bottom-left-radius: 8px;
		letter-spacing: 1px;
		white-space: pre-line;
		font-size: 14px;
	}
	.message-self .usr-message{
		max-width: calc(100% - 92px);
		margin: 4px 8px;
		color: #fff;
		background-color: #4942ad;
		padding: 8px;
		border-top-left-radius: 8px;
		border-bottom-right-radius: 8px;
		border-bottom-left-radius: 8px;
		letter-spacing: 1px;
		white-space: pre-line;
		font-size: 14px;
	}
	.message-self .usr-head{
		width: 36px;
		height: 36px;
		background-color: #4942ad;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	/*输入*/
	.input-container{
		max-height: 80px;
		width: 100%;
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		position: relative;
	}
	.input-container .input-inner{
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
	.input-container .btn{
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
		/* background: linear-gradient(to right bottom, #1c3364, #19035b); */
		background: linear-gradient(90deg, rgba(48,26,133,1) 0%, rgba(25,13,69,1) 100%);
		width: calc(100%);
		margin: 10px 0 0 0;
		padding: 10px;
		/* border: 1px solid #ccc; */
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
	.ai-head-container{
		position: absolute;
		z-index: 999;
		scale: .8;
		left: -12px;
		top: -12px;
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: #fdfdfd33;
		border-radius: 12px;
		overflow: hidden;
		backdrop-filter: blur(4px);
		box-shadow: 2px 2px 6px #00000011;
		border: 1px solid #6491f244;
	}
</style>