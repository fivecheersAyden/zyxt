<template>
	<div :class="teacherHide ? 'character-container-hide':'character-container' ">
		<!--教师角色-->
		<!--头像-->
		<!--小英老师-->
		<div class="teacher-container" v-if="(currentMode === null || currentMode === '0' || currentMode === '') && !teacherHide">
			<image v-if="!talking" src="@/static/calm.png"
				mode="aspectFit" class="taffy"></image>
			<image v-else src="@/static/speaking.gif"
				mode="aspectFit" class="taffy"></image>
		</div>
		<!--Miss White-->
		<div class="teacher-container" v-if="currentMode === '1' && !teacherHide">
			<image v-if="!talking" src="@/static/calm1.png"
				mode="aspectFit" class="taffy1"></image>
			<image v-else src="@/static/speaking1.gif"
				mode="aspectFit" class="taffy1"></image>
		</div>
		<!--Mr. Black-->
		<div class="teacher-container" v-if="currentMode === '2' && !teacherHide">
			<image v-if="!talking" src="@/static/calm2.png"
				mode="aspectFit" class="taffy2"></image>
			<image v-else src="@/static/speaking2.gif"
				mode="aspectFit" class="taffy2"></image>
		</div>
		<!--隐藏-->
		<div @click="changeTeacherHide" v-if="enableHide" class="sound-container">
			<wd-icon v-if="!teacherHide" name="fullscreen-exit" color="#fff" size="19px"></wd-icon>
			<wd-icon v-else name="arrow-right" color="#fff" size="19px"></wd-icon>
		</div>
		<!--发声组件-->
		<AliyunTTS ref="ttsRef" :role="kenny" />
	</div>
</template>

<script setup>
	import { onBeforeUnmount, onMounted, ref, watch } from 'vue';
	import { onShow, onHide } from '@dcloudio/uni-app';
	import AliyunTTS from '@/components/AliyunTTS.vue';
	
	/**
	 * 全局
	 */
	onMounted(()=>{
		talking.value = false
		getCurrentMode()
		//当前一段话首次获取消息，开始说话(强制)
		uni.$on('firstGetMessage',(msg)=>{
			ttsRef.value.clearChat()
			if(teacherHide.value) return
			console.log('语音输出开始新对话')
			updateVoice()
			addMsg(msg)
			talking.value = true
		})
		//当前一段话继续获取消息
		uni.$on('continueGetMsg', (msg)=>{
			if(teacherHide.value) return
			updateVoice()
			addMsg(msg)
		})
		uni.$on('startTalk',()=>{
			talking.value = true
		})
		//当前一段话结束
		uni.$on('endTalk',()=>{
			talking.value = false
		})
		ttsOn.value = true
	})
	onShow(()=>{
		setTimeout(()=>{
			if(!ttsOn.value){
				talking.value = false
				getCurrentMode()
				//当前一段话首次获取消息，开始说话(强制)
				uni.$on('firstGetMessage',(msg)=>{
					ttsRef.value.clearChat()
					if(teacherHide.value) return
					console.log('语音输出开始新对话')
					updateVoice()
					addMsg(msg)
					talking.value = true
				})
				//当前一段话继续获取消息
				uni.$on('continueGetMsg', (msg)=>{
					if(teacherHide.value) return
					updateVoice()
					addMsg(msg)
				})
				uni.$on('startTalk',()=>{
					talking.value = true
				})
				//当前一段话结束
				uni.$on('endTalk',()=>{
					talking.value = false
				})
				ttsOn.value = true
			}
		},200)
	})
	const ttsOn = ref(false)
	onHide(()=>{
		console.log('AI头部隐藏')
		uni.$off('firstGetMessage')
		uni.$off('continueGetMsg')
		uni.$off('startTalk')
		uni.$off('endTalk')
		if(!teacherHide.value){
			ttsRef.value.clearChat()
			ttsOn.value = false
		}
	})
	
	//是否隐藏
	const teacherHide = ref(false)
	const changeTeacherHide = ()=>{
		teacherHide.value = !teacherHide.value
		if(teacherHide.value){
			ttsRef.value.clearChat()
			ttsOn.value = false
		}
	}
	//允许隐藏
	defineProps({
		enableHide: Boolean
	})
	
	/**
	 * gif
	 */
	//获取当前教师
	const currentMode = ref('0') //'0'小英老师 '1'White '2'Black
	const getCurrentMode = ()=>{
		uni.getStorage({
			key: 'loginStorage',
			success(res) {
				currentMode.value = res.data.userInfo.country
			}
		})
	}
	//当前动图状态
	const talking = ref(false)
	/**
	 * 语音组件
	 */
	// TTS组件的ref对象
	const ttsRef = ref(null)
	//存储发给TTS组件的char
	const talkMsg = ref('')
	//切片
	const addMsg = (newChar)=>{
		talkMsg.value += newChar
		var punctuationRegex = /[^\w\s\u4e00-\u9fa5]/; // 包括非字母、非数字、非空格、非中文字符
		if(punctuationRegex.test(newChar)){
			ttsRef.value.addMsgToQueue(talkMsg.value)
			talkMsg.value = ''
		}
	}
	//更新voice
	const updateVoice = ()=>{
		let voice = 'zhixiaoxia'
		switch(currentMode.value){
			case '1': voice = 'ruoxi'
				break;
			case '2': voice = 'kenny'
				break;
			default: voice = 'zhixiaoxia'
				break;
		}
		ttsRef.value.setVoice(voice)
	}
	
</script>

<style>
	.character-container{
		width: 120px;
		height: 180px;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		transition: .6s;
	}
	.character-container .sound-container{
		position: absolute;
		bottom: 2px;
		right: 4px;
		height: 26px;
		width: 30px;
		background-color: #6290f2;
		backdrop-filter: blur(4px);
		border: 1px solid #5158de33;
		border-radius: 8px;
		display: flex;
		transition: .6s;
		align-items: center;
		justify-content: center;
		transform: translate(2px 2px);
	}
	.character-container-hide{
		width: 34px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		transition: .6s;
		background-color: transparent;
	}
	.character-container-hide .sound-container{
		position: absolute;
		bottom: 0;
		right: 0;
		height: 26px;
		width: 30px;
		background-color: #aaa;
		transition: .6s;
		backdrop-filter: blur(4px);
		border: 1px solid #5158de33;
		border-radius: 8px;
		display: flex;
		align-items: center;
		justify-content: center;
		transform: translate(2px 2px);
	}
	/*gif*/
	.teacher-container{
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}
	.teacher-container .taffy{
		height: 100%;
	}
	.teacher-container .taffy1{
		scale: 1.4;
	}
	.teacher-container .taffy2{
		scale: 1.4;
	}
</style>