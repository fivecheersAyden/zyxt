<template>
	<view class="tabbarpage-container">
		<view class="status_bar">
			<!-- 这里是状态栏 -->
		</view>
		<!-- 导航栏 -->
		<view class="page-header">
			<!-- <navigator open-type="navigateBack" hover-class="navigator-hover">
				<view class="back-icon">
					<wd-icon name="thin-arrow-left" size="18px"></wd-icon>
				</view>
			</navigator> -->
			<view class="title">
				口语听力
			</view>
			
			<!-- <view style="width: 18px">
				placeholder for symmetry
			</view> -->
		</view>

		<!--主体-->
		<view class="tabbarpage-body">
			<view class="custom-ai-container">
				<!-- 如果从首页跳入 -->
				<view v-show="fromHomeIn">
					<!-- 情景选择 -->
					<view style="font-size: 20px; font-weight: bold; margin: 0 0 15px 10px;">场景选择</view>

					<!-- 选择 -->
					<view v-for="(scene, index) in sceneList" class="card-template theme-card"
						style="margin-bottom: 15px;">
						<view class="cardcom-content" @click="select(index)">
							<view class="left">
								<view slot="avatar"
									style="width: 100px; height: 100px; border-radius: 50%; overflow: hidden;">
									<image mode="aspectFill" :src="scene.sceneImageUrl"
										style="width: 100%; height: 100%;"></image>
								</view>
							</view>

							<view class="right" style="width: 100%;">
								<view slot="content">
									<view style="display: flex; justify-content: space-between;">
										<view style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">{{
											scene.name }}</view>
										<view v-if="currentSelectedIndex == index" class="tag">当前选择</view>
									</view>
									<view style="font-size: 14px; color: #bbb;">{{ scene.description }}</view>
								</view>

							</view>
						</view>
						<wd-picker custom-class="picker-custom" v-if="currentSelectedIndex == index"
							:columns="scene.charColumns" label="你的角色" @confirm="handleConfirm" @click="hideTabbar"/>

					</view>

					<!--用户微调ai形象-->
					<view style="margin-top: 20px;">
						<input type="text" v-model="customImageText" placeholder="请输入您的期望,以调整AI教师的教学风格"
							style="border: 1px solid #ccc; padding: 10px; border-radius: 5px;" />
					</view>
					<div style="flex: 1;"></div>
					<view style="margin-top: 20px;">
						<button @click="goTalkingPg" class="choose-btn">进入沉浸式口语练习</button>
					</view>
				</view>

				<!-- 如果从练习页面返回 -->
				<view v-show="!fromHomeIn" style="height: 100%;">
					<view v-show="backMsgAvailable" >
						<AiConversationCom :isOralPractice="true" ref="aiConversationRef" />
						<view style="display: flex; justify-content: space-between; width: 100%;">
							<button class="choose-btn" @click="saveBtn">保存练习记录</button>
							<button class="choose-btn" @click="() => fromHomeIn = true">重置</button>
						</view>
					</view>
					
					<!-- <view v-show="!backMsgAvailable" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%;">
						<view style="font-size: 20px; font-weight: bold; margin-bottom: 15px;">暂无练习记录</view>
						<view style="font-size: 16px; color: #bbb;">您还没有进行过口语练习，快去体验一下吧！</view>
						<button class="choose-btn" @click="() => fromHomeIn = true">现在体验</button>
					</view> -->
					
				</view>
			</view>
		</view>
		<TabbarCom style="z-index: 0 !important;" :tabbarIndex="1" class="tabbarpage-tabbar" />
	</view>
</template>

<script setup>
import { globalProps } from '@/js/global.js'
import { ref, onMounted, onUnmounted } from 'vue'
import AiConversationCom from '@/components/AiConversationCom.vue';
import CardCom from '@/components/CardCom.vue';
import TabbarCom from '@/components/TabbarCom.vue';

const backMsgAvailable = ref(false)

/**
 * 全局
 */
onMounted(() => {
	console.log('RealTimeTalkingEntry: onMounted')
	getPrams()
	// 监听口语听力页面的事件 {
	uni.$on('backFromOralPractice', function (data) {
		console.log('监听到事件来自 backFromOralPractice', data);
		fromHomeIn.value = false;
		backMsgAvailable.value = data.msgList.length > 0
	})
	select(0)
})

/**
 * 已有
 */
// 情景选择
const myCharValue = ref('')
const gptCharValue = ref('')
const selectedMainLine = ref('')
const handleConfirm = (e) => {
	console.log('选择的角色:', e.value)
	if (selectedScene.value.charColumns[0] === e.value) {
		myCharValue.value = selectedScene.value.charColumns[0]
		gptCharValue.value = selectedScene.value.charColumns[1]
		selectedMainLine.value = selectedScene.value.main_line[0]
	} else {
		myCharValue.value = selectedScene.value.charColumns[1]
		gptCharValue.value = selectedScene.value.charColumns[0]
		selectedMainLine.value = selectedScene.value.main_line[1]
	}
	console.log('gpt角色:', gptCharValue.value)
	console.log('mainline: ', selectedMainLine.value)
}

const aiConversationRef = ref(null)

// 切换页面显示
const fromHomeIn = ref(true)

// 场景选择
const currentSelectedIndex = ref(0)
const select = (index) => {
	currentSelectedIndex.value = index
	selectedScene.value = sceneList.value[index]
	console.log('选择了场景:', selectedScene.value)
	myCharValue.value = selectedScene.value.charColumns[0]
	gptCharValue.value = selectedScene.value.charColumns[1]
	selectedMainLine.value = selectedScene.value.main_line[0]
}

const sceneList = ref([
	{
		id: 0,
		name: '购物对话',
		sceneImageUrl: '../../static/shopScene.jpeg',
		description: '在商店里和店员交流如何购买商品的对话练习，你可以扮演消费者或者收银员，去完成一次商品的购买或销售。',
		main_line: ["此时用户想要购买一件衣服，但是想要咨询它的相关信息，需要向店员询问", "此时用户是店员，可以帮助顾客选择商品"],
		charColumns: ["顾客", "店员"]
	},
	{
		id: 1,
		name: '餐厅对话',
		sceneImageUrl: '../../static/orderScene.png',
		description: '在餐厅点菜和服务员交流的对话练习，你可以扮演顾客或者服务员，去完成一次餐厅的用餐体验或服务。',
		main_line: ["此时用户想要点餐，但是不知道具体的菜单，需要向服务员询问", "此时用户是服务员，可以帮助顾客点菜"],
		charColumns: ["顾客", "服务员"]
	},
	{
		id: 2,
		name: '旅游对话',
		sceneImageUrl: '../../static/travelScene.jpg',
		description: '在旅游中和当地人交流的对话练习，你可以扮演游客或者当地人，去完成一次问路或向导指引。',
		main_line: ["此时用户想要前往海边，但是不知道具体的路线，需要向附近居民询问", "此时用户是当地居民，可以帮助游客指引路线"],
		charColumns: ["游客", "当地人"]
	}
])

const selectedScene = ref(sceneList.value[0])
/**
 * 交互
 */
//获取参数
//用户字段country为教师type，city为自定义ai教师性格
const loginStore = ref()
const token = ref()
const customImageText = ref();
const getPrams = () => {
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
const updateCurrent = (country) => {
	switch (country) {
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

// 进入口语页面
const goTalkingPg = () => {
	// 构建当前场景名、图片、角色信息
	const sceneInfo = {
		sceneName: selectedScene.value.name,
		sceneImageUrl: selectedScene.value.sceneImageUrl,
		myCharValue: myCharValue.value,
		gptCharValue: gptCharValue.value,
		customImageText: customImageText.value,
		mainLine: selectedMainLine.value
	}
	// 存储
	uni.setStorage({
		key: 'sceneInfo',
		data: JSON.stringify(sceneInfo),
		success: function () {
			console.log('存储成功')
		}
	})
	uni.navigateTo({
		url: '/pages/RealTimeTalkingPage/RealTimeTalkingPage'
	})
}

// 保存练习记录
const saveBtn = () => {
	uni.showToast({
		icon: 'success',
		title: '保存成功'
	})
}

</script>

<style>
@import url("@/css/global.css");
@import url("@/css/animation.css");


.picker-custom {
	margin-top: 15px;
	border-radius: 10px;
	background-color: rgba(255, 255, 255, 0.308);
	box-shadow: 0px 0px 8px -2px rgba(0, 0, 0, 0.1);
}

:deep(.wd-picker__cell) {
	background-color: inherit !important;
}

:deep(.wd-picker__label) {
	color: white !important;
	font-weight: bold;
}
:deep(.wd-picker__value) {
	color: white !important;
}

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

.choose-btn {
	flex: 1;
	margin: 15px 10px;
	background-color: #6255f2;
	color: #fff;
	outline: none;
	box-shadow: 2px 2px 6px #00000011;
}
</style>