<template>
	<view class="top-container">
		<!--标题-->
		<view class="welcome">
			智悦学途
		</view>
		<!--ai头像＆按钮-->
		<div class="medium-container">
			<!--ai头像-->
			<AiCharacterCom :enableHide="false" class="ai-head-container"></AiCharacterCom>
			<!--按钮-->
			<view class="entries-container">
				<!--问候-->
				<div :class="strMode ? 'cheer-container-str' : 'cheer-container-close'">
					<h1>{{ currentCheer }}</h1>
					<p>嗨，我是您的ai英语助教小英老师。我能通过对话帮助您解决问题，使用人工智能赋能您的英语学习。</p>
					<h2>全部功能</h2>
				</div>
				<!--跳转按钮-->
				<div :class="strMode? 'entry-all-str' : 'entry-all-close'">
					<!--个性ai-->
					<div @click="navCustomAi" class="entry">
						<wd-icon name="chat" size="16px"></wd-icon>
						<div>个性AI</div>
					</div>
					<!--新建讨论-->
					<div class="entry" @click="navNewQues">
						<wd-icon name="add-circle1" size="16px"></wd-icon>
						<div>新建讨论</div>
					</div>
					<!--学情分析-->
					<div class="entry" @click="navGrowPage">
						<wd-icon name="chart" size="16px"></wd-icon>
						<div>学情分析</div>
					</div>
					<!--习题推荐-->
					<div @click="navRecommand" :class="strMode? 'entry-hide' : 'entry'">
						<wd-icon name="tips" size="16px"></wd-icon>
						<div>习题推荐</div>
					</div>
					<!--温故知新-->
					<div @click="navConsolid" :class="strMode? 'entry-hide' : 'entry'">
						<wd-icon name="a-rootlist" size="16px"></wd-icon>
						<div>温故知新</div>
					</div>
					<!--听力口语-->
					<div @click="navHearSpeak" :class="strMode? 'entry-hide' : 'entry'">
						<wd-icon name="service" size="16px"></wd-icon>
						<div>口语听力</div>
					</div>
					<!--历史对话-->
					<div @click="navHistory" :class="strMode? 'entry-hide' : 'entry'">
						<wd-icon name="history" size="16px"></wd-icon>
						<div>历史对话</div>
					</div>
					<!--个人中心-->
					<div @click="navMinePage" :class="strMode? 'entry-hide' : 'entry'">
						<wd-icon name="home" size="16px"></wd-icon>
						<div>个人中心</div>
					</div>
					<!--收缩展开按钮-->
					<div class="mode-btn" v-if="strMode" @click="changeStrMode">
						<wd-icon name="more1" size="18px"></wd-icon>
					</div>
					<div @click="changeStrMode" :class="strMode? 'entry-hide' : 'entry'" style="background-color: #4d80f088; border: 1px solid transparent;">
						<wd-icon name="arrow-right" size="16px"></wd-icon>
						<div>收起</div>
					</div>
				</div>
			</view>
			
		</div>
		<!--对话-->
		<div class="ai-cvs-self">
			<AiConversationCom @only-read="isCalm = false"
			@only-stop="isCalm = true" :homepage-prompt="true" />
		</div>
		
	</view>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import AiConversationCom from '../../../components/AiConversationCom.vue';
import { globalProps } from '@/js/global.js'
import AiCharacterCom from '@/components/AiCharacterCom.vue'

onMounted(()=>{
	setCurrentCheer()
})

//显示模式
const strMode = ref(true)
const changeStrMode = ()=>{
	strMode.value = !strMode.value
}
//当前时间
const currentCheer = ref('')
const setCurrentCheer = ()=>{
	const now = new Date();
	const hour = now.getHours();
	if (hour < 12) {
		currentCheer.value = 'Good morning'
	} else if (hour < 18) {
		currentCheer.value = 'Good afternoon'
	} else {
		currentCheer.value = 'Good evening'
	}
}

const src = ref('')
// const textSubmit = ref('')
const isCalm = ref(true)

// 页面跳转
const navNewQues = () => {
	uni.navigateTo({
		url: "/pages/NewQuesPage/NewQuesPage"
	})
}
const navGrowPage = () => {
	uni.navigateTo({
		url: '/pages/GrowPage/GrowPage'
	})
}
const navHistory = () => {
	uni.navigateTo({
		url: "/pages/HistoryDialoguePage/HistoryDialoguePage"
	})
}
const navConsolid = () => {
	uni.navigateTo({
		url: "/pages/ReviewPage/ReviewPage"
	})
}
const navMinePage = () => {
	uni.navigateTo({
		url: "/pages/MinePage/MinePage"
	})
}
const navRecommand = ()=>{
	uni.navigateTo({
		url: "/pages/RecommandPage/RecommandPage"
	})
}
const navCustomAi = ()=>{
	uni.navigateTo({
		url: "/pages/CustomAiPage/CustomAiPage"
	})
}
const navHearSpeak = ()=>{
	uni.navigateTo({
		url: '/pages/RealTimeTalkingPage/RealTimeTalkingEntry'
	})
}


// 这部分还放在这里
const getAudioUrl = (text) => {
	// #ifdef MP-WEIXIN
	let reg = /<[^>]+>/gi;//去除富文本的标签正则
	let overText = "";
	if (text) {
		overText = text.replace(reg, '');
	}

	let plugin = requirePlugin("WechatSI")
	let manager = plugin.getRecordRecognitionManager();

	plugin.textToSpeech({
		lang: "zh_CN",//中文 当然还可以换成其他语言读出
		tts: true,
		content: overText,//要读的内容
		success: (res) => {
			console.log("succ tts: ", res.filename)
			src.value = res.filename;//生成的地址路径
			getInnerAudioContext(src.value)
		}
	})
	// #endif
	// #ifndef MP-WEIXIN
	// 语音合成
	uni.showToast({
		title: '暂不支持语音合成',
		icon: 'none'
	})
	// #endif
}

const innerAudioContext = uni.createInnerAudioContext();

const getInnerAudioContext = (url) => {
	innerAudioContext.obeyMuteSwitch = false;
	innerAudioContext.autoplay = true;
	innerAudioContext.src = url;
	console.log(innerAudioContext)
	if (innerAudioContext.paused) {
		isCalm.value = false;
		innerAudioContext.play();
	} else {
		innerAudioContext.pause();
	}
	innerAudioContext.onEnded(() => {
		isCalm.value = true;
		innerAudioContext.seek = 0;
	})

}

</script>

<style>
.top-container {
	position: absolute;
	left: 20px;
	right: 20px;
	top: 8px;
	bottom: 12px;
	display: flex;
	flex-direction: column;
}

/*顶部*/
.welcome {
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
	font-family: "San Francisco", Rotobo, arial, "PingFang SC", "Noto SansCJK", "Microsoft Yahei", sans-serif;
	font-size: 21px;
	font-weight: bold;
	height: 40px;
	letter-spacing: 2px;
}
/* 中间 */
.medium-container{
	position: absolute;
	left: 0;
	right: 0;
	top: 46px;
	height: 180px;
	display: flex;
	align-items: center;
	justify-content: space-between;
}
/*ai头部*/
.ai-head-container{
	margin: 0 20px 0 0;
}

/*ai按钮*/
.entries-container{
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: space-between;
	height: 100%;
	flex: 1;
	margin-right: 4px;
}
.cheer-container-str{
	height: calc(100% - 52px);
	width: 100%;
	transition: .6s;
}
.cheer-container-str h1{
	font-size: 24px;
	letter-spacing: 1px;
	margin: 4px 0;
	transition: .6s;
}
.cheer-container-str p{
	font-size: 13px;
	color: #666;
	letter-spacing: 1px;
	transition: .6s;
}
.cheer-container-str h2{
	scale: 0;
	transition: .6s;
	opacity: 0;
	transform: translateY(-20px);
}
.cheer-container-close{
	height: 32px;
	width: 100%;
	transition: .6s;
	color: #000;
}
.cheer-container-close h1{
	height: 0;
	font-size: 0;
	letter-spacing: 1px;
	margin: 4px 0;
	transition: .6s;
	opacity: 0;
	margin: 0;
}
.cheer-container-close p{
	height: 0;
	font-size: 0;
	transition: .6s;
	opacity: 0;
	margin: 0;
}
.cheer-container-close h2{
	font-size: 13px;
	transition: .6s;
	color: #666;
	letter-spacing: 2px;
	transform: translateY(8px);
}

.entry-all-str{
	flex: 1;
	display: flex;
	width: 100%;
	align-items: center;
	justify-content: space-between;
	transition: .6s;
	flex-wrap: wrap;
}
.entry-all-close{
	flex: 1;
	display: flex;
	width: 100%;
	align-items: center;
	justify-content: space-between;
	transition: .6s;
	flex-wrap: wrap;
}
.mode-btn{
	width: 20px;
	background-color: #4d80f088;
	border-radius: 12px;
	box-shadow: 2px 2px 6px #00000022;
	display: flex;
	align-items: center;
	justify-content: center;
	color: #fff;
	height: 32px;
	padding: 4px 0;
}
.entry{
	display: flex;
	align-items: center;
	justify-content: space-between;
	flex-direction: column;
	color: #fff;
	font-size: 11px;
	height: 32px;
	padding: 4px 0;
	width: calc(32% - 12px);
	background-color: #4d80f0dd;
	border-radius: 8px;
	box-shadow: 2px 2px 6px #00000022;
	border: 1px solid #6a75de;
	transition: 1s;
}
.entry-hide{
	opacity: 0;
	display: none;
	transition: 1s;
}


/*对话*/
.login-prompt {
	padding: 5px 10px;
	background-color: #ccc;
	border-radius: 5px;
}
.ai-cvs-self {
	position: absolute;
	bottom: 0;
	left: 0;
	right: 0;
	top: 236px;
}
</style>