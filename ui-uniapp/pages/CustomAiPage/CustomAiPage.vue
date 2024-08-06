<template>
	<view class="tabbarpage-container">
		<view class="status_bar">
			<!-- 这里是状态栏 -->
		</view>
		<!-- 导航栏 -->
		<view class="page-header-back">
			<navigator open-type="navigateBack" hover-class="navigator-hover">
				<view class="back-icon">
					<wd-icon name="thin-arrow-left" size="18px"></wd-icon>
				</view>
			</navigator>
			<view class="title">
				个性AI
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<view class="custom-ai-container">
				<!--选择-->
				<view v-for="(aiItem, index) in aiList" class="card-template theme-card" style="margin-bottom: 15px;">
					<view class="cardcom-content" @click="select(index)">
						<!-- 人物头像 -->
						<view class="left">
							<view slot="avatar"
								style="width: 100px; height: 100px; border-radius: 50%; overflow: hidden;">
								<!-- 静止 -->
								<image v-if="aiItem.isCalm" mode="aspectFit" :src="aiItem.calmAvatarUrl" style="width: 100%; height: 100%;">
								</image>
								<!-- 说话 -->
								<image v-else mode="aspectFit" :src="aiItem.speakingAvatarUrl" style="width: 100%; height: 100%;">
								</image>
							</view>
						</view>
						<!-- 说明信息 -->
						<view class="right">
							<view slot="content">
								<view style="display: flex; justify-content: space-between;">
									<view style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">{{
										aiItem.name }}</view>
									<view v-if="currentSelectedIndex == index" class="tag">
										当前选择
									</view>
								</view>
								<view style="font-size: 14px; color: #666;">{{ aiItem.characteristic }}</view>
							</view>
						</view>
					</view>
				</view>
				<!--用户微调ai形象-->
				<view style="margin-top: 20px;">
					<input type="text" v-model="customImageText" placeholder="请输入您的期望,以调整AI教师的教学风格"
						style="border: 1px solid #ccc; padding: 10px; border-radius: 5px;" />
				</view>
				<div style="flex: 1;"></div>
				<view style="margin-top: 20px;">
					<button @click="btnSure" class="choose-btn">完成个性AI自定义</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script setup>
import { globalProps } from '@/js/global.js'
import { ref, onMounted, onUnmounted } from 'vue'

/**
 * 全局
 */
onMounted(()=>{
	getPrams()
})

/**
 * 已有
 */
const currentSelectedIndex = ref(0)
const select = (index) => {
	currentSelectedIndex.value = index
}
const aiList = ref([
	{
		id: 0,
		name: '小英老师',
		calmAvatarUrl: '../../static/calm.png',
		speakingAvatarUrl: '../../static/speaking.gif',
		characteristic: '小英老师是一位非常有耐心的老师，她擅长启发式教学，会耐心的解答你的问题，帮助你学习英语。',
		isCalm: true
	},
	{
		id: 1,
		name: 'Miss White',
		calmAvatarUrl: '../../static/calm1.png',
		speakingAvatarUrl: '../../static/speaking1.gif',
		characteristic: 'Miss White 虽然严厉，但善于发现学生的英语薄弱点，能够在你的学习遇到困惑时给出精确及时的帮助。',
		isCalm: true
	},
	{
		id: 2,
		name: 'Mr. Black',
		calmAvatarUrl: '../../static/calm2.png',
		speakingAvatarUrl: '../../static/speaking2.gif',
		characteristic: 'Mr. Black 是一位非常有趣的老师，他擅长和学生交朋友，会用生动有趣的教学方式让你爱上英语。',
		isCalm: true
	}
])
/**
 * 交互
 */
//获取参数
//用户字段country为教师type，city为自定义ai教师性格
const loginStore = ref()
const token = ref()
const customImageText = ref();
const getPrams = ()=>{
	uni.getStorage({
		key: 'loginStorage',
		success(res) {
			loginStore.value = res.data
			token.value = res.data.token
			updateCurrent(res.data.userInfo.country)
			customImageText.value = res.data.userInfo.city
		}
	})
}
//获取字段后更新渲染
const updateCurrent = (country)=>{
	switch(country){
		case '1':
			select(1)
			break;
		case '2':
			select(2)
			break;
		default: 
			select(0)
			break;
	}
}

//上传定义
const btnSure = ()=>{
	loginStore.value.userInfo.country = currentSelectedIndex.value.toString()
	loginStore.value.userInfo.city = customImageText.value
	uni.request({
		url: globalProps.baseApi + 'users',
		method: 'PUT',
		header:{
			Authorization: 'Bearer ' + token.value
		},
		data:loginStore.value.userInfo,
		success(res) {
			if(res.statusCode !== 200){
				console.log('更新失败', res)
				uni.showToast({
					icon: 'error',
					title: '更新失败'
				})
			}
			uni.showToast({
				icon: 'success',
				title: '更改成功'
			})
			uni.setStorage({
				key: 'loginStorage',
				data: loginStore.value
			})
		},
		fail(e) {
			console.log('更新失败', e)
			uni.showToast({
				icon: 'error',
				title: '更新失败'
			})
		}
	})
}

</script>

<style>
@import url("@/css/global.css");
@import url("@/css/animation.css");

.custom-ai-container {
	position: absolute;
	display: flex;
	flex-direction: column;
	top: 8px;
	right: 8px;
	bottom: 16px;
	left: 8px;
}

.cardcom-content {
	display: flex;
	align-items: center;
	gap: 15px;
}

.tag {
	height: fit-content;
	border-radius: 10px;
	background-color: #6255f2;
	color: white;
	padding: 2px 8px;
}

.card-template {
	display: flex;
	flex-direction: column;
	padding: 15px;
	border-radius: 15px;
	margin-bottom: 20px;
}
.choose-btn{
	background-color: #6255f2;
	color: #fff;
	outline: none;
	box-shadow: 2px 2px 6px #00000011;
}
</style>