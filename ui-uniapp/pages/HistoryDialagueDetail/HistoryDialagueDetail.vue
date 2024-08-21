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
				{{quesDialogue.question.questime}} 问题对话
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>
		</view>
		<!--主体-->
		<view style="margin-bottom: 24px;"  class="tabbarpage-body">
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
				<!--相似-->
				<!-- <div :class="showQues ? 'photo-btn-bottom' : 'photo-btn-top'" @click="jumpToSimilarHistory">
					相似历史
					<wd-icon style="margin: 2px 0 0 6px;" color="#fff" name="history" size="26px"></wd-icon>
				</div> -->
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
	
	/**
	 * 全局
	 */
	onLoad((e)=>{
		getCurrentQues(e)
		//底部动画
		setTimeout(()=>{
			showQues.value = false
		},200)
	})
	onBeforeUnmount(()=>{
		saveDialogue()
	})
	//保存参数
	const savePrams = ref({
		id: null,
		token: null
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
	//保存
	const saveDialogue = ()=>{
		quesDialogue.value.dialogs = quesAiConversation.value.getDialogues()
		console.log('保存对话参数',quesDialogue.value)
		uni.request({
			url: globalProps.baseApi + 'question',
			method: 'PUT',
			header: {
			        'Authorization': 'Bearer ' + savePrams.value.token
			},
			data: quesDialogue.value,
			success() {
				uni.showToast({
					icon: 'success',
					title: '保存成功'
				})
			},
			fail() {
				uni.showToast({
					icon: 'error',
					title: '保存失败'
				})
			}
		})
	}
	
	/**
	 * 对话
	 */
	const quesAiConversation = ref()
	
	/**
	 * 问题
	 */
	const customNewQues = ref()
	//获取问题
	const getCurrentQues = (e)=>{
		console.log('获取题目参数',e)
		savePrams.value.id = e.stuID
		savePrams.value.token = e.token
		uni.request({
			url: globalProps.baseApi + 'question/detail',
			method: 'GET',
			header: {
			        'Authorization': 'Bearer ' + e.token
			},
			data:{
				questionID: e.questionID,
				stuID: e.stuID
			},
			success(res) {
				console.log('获取题目结果',res)
				quesDialogue.value = res.data
				//更新题目
				customNewQues.value.updateCustomNewQues(res.data.cuoTiJi)
				//更新对话
				quesAiConversation.value.setDialogs(res.data.dialogs)
				//对话滑动到最底
				setTimeout(()=>quesAiConversation.value.scrollToBottomExpose(),300)
			},
			fail(e) {
				uni.showToast({
					icon: 'error',
					title: '获取题目失败'
				})
				console.log('获取题目细节失败',e)
			}
		})
	}
	
	//相似历史
	const jumpToSimilarHistory = ()=>{
		uni.showLoading({
			title: '寻找相关问题历史'
		})
		//未完成
		setTimeout(()=>{
			uni.hideLoading()
			uni.navigateTo({
				url: '/pages/NewQuesPage/SimilarHistory/SimilarHistory'
			})
		}, 2000)
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
		background: linear-gradient(to top, #1b1941, #2d2874);
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
	.photo-btn-top{
		position: fixed;
		right: 4px;
		bottom: 80px;
		background-color: #6b49f0bb;
		width: 120px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 2px 2px 4px #00000011;
		border-radius: 8px;
		transition: .6s;
		color: #fff;
	}
	.photo-btn-bottom{
		position: fixed;
		right: 4px;
		bottom: 12px;
		background-color: #6b49f0bb;
		width: 120px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 2px 2px 4px #00000011;
		border-radius: 8px;
		transition: .6s;
		color: #fff;
	}

</style>
