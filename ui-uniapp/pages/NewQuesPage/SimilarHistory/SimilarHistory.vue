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
			<view class="title" style="font-size: 14px;">
				历史对话 {{ historyDialogs[currentDialogQuesIndex].question.questime }}
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<!--对话-->
			<div class="dialogue-container">
				<QuesAiConversationCom ref="quesAiConversation" :conversationType="0" class="dialogue-self"></QuesAiConversationCom>
			</div>
			<!-- 问题-->
			<div :class="showQues? 'ques-container' : 'ques-container-hide'">
				<!--收缩展开按钮-->
				<wd-icon name="arrow-down" @click="changeShowQues" v-if="showQues" size="22px"></wd-icon>
				<wd-icon name="arrow-up" color="#fff" @click="changeShowQues" v-else size="22px"></wd-icon>
				<!--问题组件-->
				<div class="ques-line-container">
					<!--新问题-->
					<CustomNewQues :mode="0" ref="customNewQues" :customNewQues="quesDialogue.cuoTiJi"></CustomNewQues>
				</div>
			</div>
			<!--选择按钮-->
			<div :class="showQues?'photo-container-before':'photo-container-after'">
				<div class="photo-btn" @click="lastQues">
					<wd-icon color="#fff" name="arrow-left" size="28px"></wd-icon>
				</div>
				<div class="photo-btn">
					{{ currentDialogQuesIndex+1 }}
				</div>
				<div class="photo-btn" @click="nextQues">
					<wd-icon color="#fff" name="arrow-right" size="28px"></wd-icon>
				</div>
			</div>
		</view>
	</view>
</template>

<script setup>
	import { globalProps } from '@/js/global.js';
	import { onBeforeUnmount, onMounted, ref } from 'vue';
	import { onLoad } from '@dcloudio/uni-app'
	import CustomNewQues from '@/components/CustomNewQues.vue'
	import QuesAiConversationCom from '@/components/QuesAiConversationCom.vue'
	import {simaliarHistory} from '@/js/tmpSimaliarHistory.js'
	
	/**
	 * 全局
	 */
	onLoad((e)=>{
		getCurrentQues(e)
	})
	onMounted(()=>{
		//底部动画
		setTimeout(()=>{
			changeShowQues()
		},200)
	})
	//参数载体
	const quesDialogue = ref({
		 "cuoTiJi": {
		  "category": '',
		  "stuAnswer": ``,
		  "content": "",
		  "esID": "",
		  "aiComment":''
		},
		"dialogs": [],
		"question": {
			"questime": null,
			"stuID": 0
		},
			"stuID": 0
		})
	//收缩展开
	const showQues = ref(true)
	const changeShowQues = ()=>{
		showQues.value = !showQues.value
	}
	/**
	 * 对话
	 */
	const quesAiConversation = ref()
	
	/**
	 * 问题
	 */
	const customNewQues = ref()
	//所有相似的对话
	const historyDialogs = ref([])
	//当前题目和对话index
	const currentDialogQuesIndex = ref(0)
	//更新当前题目和对话
	const updateCurrentDialogQues = ()=>{
		quesDialogue.value = historyDialogs.value[currentDialogQuesIndex.value]
		//更新题目
		customNewQues.value.updateCustomNewQues(historyDialogs.value[currentDialogQuesIndex.value].cuoTiJi)
		//更新对话
		quesAiConversation.value.setDialogs(historyDialogs.value[currentDialogQuesIndex.value].dialogs)
		//对话滑动到最底
		setTimeout(()=>quesAiConversation.value.scrollToBottomExpose(),300)
	}
	//获取问题
	const getCurrentQues = (e)=>{
		historyDialogs.value = simaliarHistory
		updateCurrentDialogQues()
	}
	//上一题
	const lastQues = ()=>{
		if(currentDialogQuesIndex.value === 0){
			uni.showToast({
				icon: 'none',
				title: '没有上一题了'
			})
			return
		}
		currentDialogQuesIndex.value -= 1
		updateCurrentDialogQues()
	}
	//下一题
	const nextQues = ()=>{
		if(currentDialogQuesIndex.value === historyDialogs.value.length-1){
			uni.showToast({
				icon: 'none',
				title: '没有下一题了'
			})
			return
		}
		currentDialogQuesIndex.value += 1
		updateCurrentDialogQues()
	}
	
	
</script>

<style>
	@import url("@/css/global.css");
	@import url("@/css/animation.css");
	.tabbarpage-body{
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
	}
	/*对话*/
	.dialogue-container{
		margin-top: 8px;
		flex: 1;
		width: 100%;
		position: relative;
		margin-bottom: 8px;
		animation: top-in-ani .8s 1;
	}
	.dialogue-self{
		position: absolute;
		bottom: 0;
		right: 4px;
		left: 4px;
		top: 0;
	}
	/*问题*/
	.ques-container{
		height: 70%;
		width: 100%;
		background: linear-gradient(to top, #f6fbfe, #f1f5fd);
		border-top: #4d80f066 1px solid;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		transition: .6s;
		padding-top: 4px;
		border-top-left-radius: 12px;
		border-top-right-radius: 12px;
		position: relative;
	}
	.ques-container-hide{
		height: 24px;
		width: 100%;
		background-color: #4d80f0dd;
		transition: .6s;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding-top: 4px;
		border-top-left-radius: 12px;
		border-top-right-radius: 12px;
	}
	.ques-line-container{
		flex: 1;
		width: calc(100% - 12px);
		margin: 4px 4px 8px 4px;
		overflow-y: scroll;
		overflow-x: hidden;
		position: relative;
	}
	.photo-container-before{
		z-index: 9999;
		position: fixed;
		right: -28px;
		bottom: 0;
		border-radius: 8px;
		width: 240px;
		height: 50px;
		opacity: 1;
		scale: 0.7;
		transition: .6s;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.photo-container-after{
		z-index: 999;
		position: fixed;
		right: -28px;
		bottom: 80px;
		border-radius: 8px;
		width: 240px;
		height: 50px;
		opacity: 1;
		scale: 0.7;
		transition: .6s;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.photo-container-after .photo-btn,
	.photo-container-before .photo-btn{
		width: 72px;
		height: 50px;
		background-color: #5b50f0dd;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 8px;
		box-shadow: 2px 2px 6px #00000011;
		color: #fff;
		font-size: 20px;
	}

</style>
