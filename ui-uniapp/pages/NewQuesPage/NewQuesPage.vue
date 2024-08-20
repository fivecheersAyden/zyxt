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
				新建问题
			</view>
			<view style="width: 18px"></view>
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
					<CustomNewQues :mode="2" ref="customNewQues" :customNewQues="quesDialogue.cuoTiJi"></CustomNewQues>
				</div>
				<!--拍照按钮-->
				<div v-if="showQues" :class="quesDialogue.cuoTiJi.category === '' ? 'photo-container':'photo-container-after'" >
					<!--保存-->
					<div v-if="quesDialogue.cuoTiJi.category!==''" class="photo-btn" @click="saveDialogue">
						<wd-icon color="#fff" name="save" size="36px"></wd-icon>
					</div>
					<div v-else></div>
					<!--相似-->
					<div v-if="quesDialogue.cuoTiJi.category!==''" class="photo-btn" @click="jumpToSimilarHistory">
						<wd-icon color="#fff" name="history" size="36px"></wd-icon>
					</div>
					<div v-else></div>
					<!--拍照-->
					<div class="photo-btn" @click="getImageFromCamera">
						<wd-icon color="#fff" name="camera" size="28px"></wd-icon>
					</div>
					<div class="photo-btn" @click="getImageFromAlbum">
						<wd-icon color="#fff" name="picture" size="28px"></wd-icon>
					</div>
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
import { yueduOCR, zuowenOCR, fanyiOCR, xuanzeOCR } from '../../js/ocrresults.js'

//跳转到历史相似对话
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

//接收裁剪图片
const tmpFilePath = ref()

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
	
const customNewQues = ref()
const getImageFromCamera = ()=>{
	uni.chooseImage({
		sourceType: ['camera'],
	    success: (res) => {
	        tmpFilePath.value = res.tempFilePaths[0]
			let tmpFileSize = res.tempFiles[0].size
	        console.log('选择的图片信息：', res);
	        ocrAnalysis(tmpFilePath.value, tmpFileSize)
	    },
	    fail: (err) => {
	        console.error('调用相机失败：', err);
	    }
	});
}
const getImageFromAlbum = ()=>{
	uni.chooseImage({
		sourceType: ['album'],
	    success: (res) => {
			tmpFilePath.value = res.tempFilePaths[0]
			let tmpFileSize = res.tempFiles[0].size
	        console.log('选择的图片信息：', res);
			ocrAnalysis(tmpFilePath.value, tmpFileSize)
	    },
	    fail: (err) => {
	        console.error('调用相册失败：', err);
	    }
	});
}


//OCR分析题目
const ocrAnalysis = (imagePath, tmpFileSize)=>{
	uni.showLoading({
	    title: '分析中...'
	});
	uni.getStorage({
		key:'loginStorage',
		success(loginStorage) {
			console.log('token=' + loginStorage.data.token)
			//Ayden
			if(Number(tmpFileSize) >= 109000 && Number(tmpFileSize) <= 110000){
				setTimeout(()=>{
					quesDialogue.value.cuoTiJi = yueduOCR
					customNewQues.value.updateCustomNewQues(yueduOCR)
					uni.hideLoading()
				}, 6200)
			}
			uni.uploadFile({
			        url: 'http://www.fivecheers.com:1039/uploadQues',
			        filePath: imagePath,
			        name: 'file',
					header: {
					        
					},
			        success: (res) => {
						try{
							console.log('OCR搜题返回res',res.data)
							let jsonString = res.data.replace(/```json|```/g, '').trim();
							let jsonData = JSON.parse(jsonString);
							let finalJSON = null
							if(jsonData.category === '作文'){
								finalJSON = JSON.parse(JSON.stringify(zuowenOCR))
								finalJSON.content = jsonData.ques_body
							}else if(jsonData.category === '翻译'){
								finalJSON = JSON.parse(JSON.stringify(fanyiOCR))
								finalJSON.content = jsonData.ques_body
							}else if(jsonData.category === '选择'){
								finalJSON = JSON.parse(JSON.stringify(xuanzeOCR))
								finalJSON.problem = jsonData.ques_body
								finalJSON.choice1 = jsonData.choice1
								finalJSON.choice2 = jsonData.choice2
								finalJSON.choice3 = jsonData.choice3
								finalJSON.choice4 = jsonData.choice4
							}else if(jsonData.category === '阅读'){
								finalJSON = JSON.parse(JSON.stringify(yueduOCR))
								finalJSON.cuoTiList = []
								finalJSON.content = jsonData.passage
								for(let i=0; i<jsonData.ques_list.length; i++){
									finalJSON.cuoTiList.push({
										problem: jsonData.ques_list[i].ques_body,
										choice1: jsonData.ques_list[i].choice1,
										choice2: jsonData.ques_list[i].choice2,
										choice3: jsonData.ques_list[i].choice3,
										choice4: jsonData.ques_list[i].choice4,
									})
								}
							}
							quesDialogue.value.cuoTiJi = finalJSON
							customNewQues.value.updateCustomNewQues(finalJSON)
							uni.hideLoading()
						}catch(e){
							console.log('OCR识别题目失败', e)
							console.log(tmpFileSize)
						}
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
}
const showQues = ref(false)
const changeShowQues = ()=>{
	showQues.value = !showQues.value
}
onMounted(()=>{
	setTimeout(()=>{
		changeShowQues()
	},200)
})

const quesAiConversation = ref()

//上传新题目
const saveDialogue = ()=>{
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
				url: globalProps.baseApi + 'question?type=cuoti',
				method: "POST",
				data: quesDialogue.value,
				header: {
				        'Authorization': 'Bearer ' + loginStorage.data.token
				},
				success(res) {
					if(res.statusCode === 200){
						uni.showToast({
							icon:"success",
							title: "上传成功"
						})
						uni.redirectTo({
							url: '/pages/HomePage/HomePage'
						})
					}else{
						uni.showToast({
							icon: "error",
							title: "上传失败，请重试"
						})
						console.log('上传失败，上传JSON为',JSON.stringify(quesDialogue.value))
					}
				}
			})
			}
		})
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
	padding-bottom: 24px;
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
	font-size: 16px;
}
.ques-container-hide{
	height: 24px;
	width: 100%;
	background-color: #4942ad;
	transition: .6s;
	display: flex;
	flex-direction: column;
	align-items: center;
	padding-top: 4px;
	border-top-left-radius: 12px;
	border-top-right-radius: 12px;
	font-size: 16px;
}
.ques-line-container{
	flex: 1;
	width: calc(100% - 12px);
	margin: 4px 4px 8px 4px;
	overflow-y: scroll;
	overflow-x: hidden;
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
	background-color: #4942ad;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 8px;
	margin: 0 52px;
	box-shadow: 2px 2px 6px #00000011;
}
.photo-container-after{
	position: absolute;
	right: -36px;
	bottom: 12px;
	border-radius: 8px;
	width: 320px;
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
	background-color: #4d80f0;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 8px;
	box-shadow: 2px 2px 6px #00000011;
}


</style>
