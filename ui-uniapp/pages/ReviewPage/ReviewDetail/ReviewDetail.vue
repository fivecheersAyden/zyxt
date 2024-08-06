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
				复习 {{currentQuesIndex + 1}}/{{recommandQuesList.length}}
			</view>
			<view style="width: 18px"></view>
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<!--问题-->
			<div class="dialogue-container">
				<!--新问题-->
				<CustomNewQues :mode="1" ref="customNewQues" :customNewQues="quesDialogue.cuoTiJi"></CustomNewQues>
				<!--选择按钮-->
				<div v-if="quesDialogue.cuoTiJi.category!==''" class="photo-container-after" >
					<div class="photo-btn" @click="saveDialogue">
						<wd-icon color="#fff" name="save" size="36px"></wd-icon>
					</div>
					<div class="photo-btn" @click="lastQues">
						<wd-icon color="#fff" name="arrow-left" size="28px"></wd-icon>
					</div>
					<div class="photo-btn" @click="nextQues">
						<wd-icon color="#fff" name="arrow-right" size="28px"></wd-icon>
					</div>
				</div>
			</div>
			<!--对话-->
			<div :class="showQues? 'ques-container' : 'ques-container-hide'">
				<!--收缩展开按钮-->
				<wd-icon name="arrow-down" @click="changeShowQues" v-if="showQues" size="22px"></wd-icon>
				<wd-icon name="arrow-up" color="#fff" @click="changeShowQues" v-else size="22px"></wd-icon>
				<!--问题组件-->
				<div class="ques-line-container">
					<QuesAiConversationCom ref="quesAiConversation" :conversationType="0" class="dialogue-self"></QuesAiConversationCom>
				</div>
			</div>
		</view>
	</view>
</template>

<script setup>
import { globalProps } from '@/js/global.js'
import { onMounted, ref } from 'vue';
import QuesAiConversationCom from '@/components/QuesAiConversationCom.vue'
import CustomNewQues from '@/components/CustomNewQues.vue'
import { onLoad } from '@dcloudio/uni-app'


/**
 * 全局
 */
onMounted(()=>{
	setTimeout(()=>{
		changeShowQues()
	},200)
	getIdAndToken()
})

//id和token
const id = ref()
const token = ref()
const getIdAndToken = ()=>{
	uni.getStorage({
		key: 'loginStorage',
		success(res) {
			id.value = res.data.userInfo.id
			token.value = res.data.token
			getRecommandQues()
		}
	})
}
//展示题目
const showQues = ref(true)
const changeShowQues = ()=>{
	showQues.value = !showQues.value
}
//临时占位
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
//上传新题目
//保存记录
const saveRecord = ref([])
const saveDialogue = ()=>{
	if(saveRecord.value.includes(currentQuesIndex.value)){
		uni.showToast({
			icon: 'none',
			title: '不能重复保存'
		})
		return
	}
	quesDialogue.value.cuoTiJi = customNewQues.value.getCustomNewQues()
	quesDialogue.value.dialogs = quesAiConversation.value.getDialogues()
	uni.getStorage({
		key:'loginStorage',
		success(loginStorage) {
			console.log('token=' + loginStorage.data.token)
			console.log('userId=' + loginStorage.data.userInfo.id)
			quesDialogue.value.stuID = loginStorage.data.userInfo.id
			quesDialogue.value.question.stuID = loginStorage.data.userInfo.id
			console.log('上传当前对话',JSON.stringify(quesDialogue.value))
			uni.request({
				url: globalProps.baseApi + 'redoRecord/v3',
				method: "POST",
				data: quesDialogue.value.cuoTiJi,
				header: {
				        'Authorization': 'Bearer ' + loginStorage.data.token
				},
				success(res) {
					if(res.statusCode === 200){
						uni.showToast({
							icon:"success",
							title: "pass"
						})
						saveRecord.value.push(currentQuesIndex.value)
					}else{
						uni.showToast({
							icon: "error",
							title: "保存失败，请重试"
						})
						console.log('上传失败，上传JSON为',JSON.stringify(quesDialogue.value))
					}
				}
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
//推荐习题
const recommandQuesList = ref([])
//获取推荐习题
const getRecommandQues = ()=>{
	uni.showLoading({
		title: '获取今日复习习题'
	})
	console.log('token', token.value)
	uni.request({
		url: globalProps.baseApi + 'cuotiji/cuotiForRedo?userID=' + id.value,
		header: {
		        'Authorization': 'Bearer ' + token.value
		},
		success(res) {
			uni.hideLoading()
			if(res.statusCode === 200){
				recommandQuesList.value = res.data
				updateCurrentQues()
				console.log('获取复习习题成功', recommandQuesList.value)
			}else{
				uni.hideLoading()
				console.log('获取复习习题失败',res)
				uni.showToast({
					icon: 'error',
					title: '获取复习习题失败'
				})
			}
		},fail(e) {
			uni.hideLoading()
			console.log('获取复习习题失败',e)
			uni.showToast({
				icon: 'error',
				title: '获取复习习题失败'
			})
		}
	})
}
//更新当前题目
const updateCurrentQues = ()=>{
	quesDialogue.value.cuoTiJi = recommandQuesList.value[currentQuesIndex.value]
	customNewQues.value.updateCustomNewQues(recommandQuesList.value[currentQuesIndex.value])
}
//当前题目的index
const currentQuesIndex = ref(0)
//上一题
const lastQues = ()=>{
	if(currentQuesIndex.value === 0){
		uni.showToast({
			icon: 'none',
			title: '没有上一题了'
		})
		return
	}
	currentQuesIndex.value -= 1
	updateCurrentQues()
}
//下一题
const nextQues = ()=>{
	if(currentQuesIndex.value === recommandQuesList.value.length - 1){
		uni.showToast({
			icon: 'none',
			title: '没有下一题了'
		})
		return
	}
	currentQuesIndex.value += 1
	updateCurrentQues()
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
	overflow-y: scroll;
	overflow-x: hidden;
	width: calc(100% - 16px);
	margin: 0 8px;
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
	height: 60%;
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
	position: relative;
}
.photo-container{
	position: absolute;
	left: 0;
	right: 0;
	bottom: 0;
	top: 0;
	background-color: #ffffff22;
	backdrop-filter: blur(4px);
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: .6s;
}
.photo-container .photo-btn{
	width: 72px;
	height: 50px;
	background-color: #4d80f0;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 8px;
	margin: 0 52px;
	box-shadow: 2px 2px 6px #00000011;
}
.photo-container-after{
	z-index: 999;
	position: fixed;
	right: -24px;
	bottom: 48px;
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
.photo-container-after .photo-btn{
	width: 72px;
	height: 50px;
	background-color: #4d80f0dd;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 8px;
	box-shadow: 2px 2px 6px #00000011;
}


</style>
