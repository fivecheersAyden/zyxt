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
				温故知新
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>

		</view>

		<!--主体-->
		<view class="tabbarpage-body scrollable-padding">
			<view class="entries">
				<!-- 右下角+按钮 -->
				<view class="aistudy-pg-card" @click="getAllRedoThenJump">
					<wd-icon name="add" size="22px" color="white"></wd-icon>
				</view>
				<!-- <view class="aistudy-pg-card" @click="navigateToPage">
					<view>自定义</view>
				</view> -->
			</view>

			<view class="aistudy-pg-container">
				<view style="font-size: 40rpx; font-weight: bold; margin: 30rpx 20rpx;">历史记录</view>
				<up-search :show-action="true" actionText="搜索" :animation="true" bgColor="#473189" color="#FFFFFF"
					actionStyle="color:#FFFFFF"></up-search>

				<div class="scroll-container" v-if="currentRedoList && currentRedoList.length !== 0">
					<!-- 题目列表 -->
					<view v-for="(item, index) in currentRedoList" :key="index"
						@click="redoHistoryJump(item.id, item.redoID, item.category, item)">
						<view v-if="item.category == 'xuanze'" class="redoItem">
							<view class="item-head">
								<view class="tag">选择</view>
								<!-- <view class="tag">重做{{ item.redoNum }}次</view> -->
								<view class="false-reason">错因：{{ item.falseReason }}</view>
							</view>

							<view class="question-self">{{ item.problem }}</view>
							<view class="choice">{{ item.choice1 }}</view>
							<view class="choice">{{ item.choice2 }}</view>
							<view class="choice">{{ item.choice3 }}</view>
							<view class="choice">{{ item.choice4 }}</view>

						</view>
						<view v-else-if="item.category == 'yuedu'" class="redoItem">
							<view class="item-head">
								<view class="tag">阅读</view>
								<!-- <view class="tag">重做{{ item.redoNum }}次</view> -->
								<view class="false-reason">错因：{{ item.falseReason }}</view>
							</view>
							<view class="question-self">{{ item.content }}</view>

						</view>
						<view v-else-if="item.category == 'fanyi'" class="redoItem">
							<view class="item-head">
								<view class="tag">翻译</view>
								<!-- <view class="tag">重做{{ item.redoNum }}次</view> -->
								<view class="false-reason">错因：{{ item.falseReason }}</view>
							</view>
							<view class="question-self">{{ item.content }}</view>

						</view>
						<view v-else-if="item.category == 'zuowen'" class="redoItem">
							<view class="item-head">
								<view class="tag">作文</view>
								<!-- <view class="tag">重做{{ item.redoNum }}次</view> -->
								<view class="false-reason">错因：{{ item.falseReason }}</view>
							</view>
							<view class="question-self">{{ item.content }}</view>

						</view>
					</view>
					<!-- <div v-if="loaded" @click="quesPageJump(item.quesId)" class="ques-line dark-purple-card"
						v-for="item in currentQuesList" :key="item.quesId">
						<div style="justify-content: space-between;" class="ques-line-line">
							<div class="ques-header">{{ item.quesRemark }}</div>
							<div class="ques-time">{{ item.addTime }}</div>
						</div>
						<div class="ques-line-line">
							<div class="tag" v-for="tag in item.tags">
								{{ tag }}
							</div>
						</div>
						<div class="ques-line-line line-line-display">
							{{ item.quesDisplay }}
						</div>
					</div>
					<div v-for="i in 5" style="height: 100%; justify-content: space-around; padding: 12px;"
						class="ques-line dark-purple-card" v-else>
						<wd-skeleton theme="paragraph" />
					</div>
					<div class="more-btn">- 更多 -</div> -->

					<!-- 翻页组件 -->
				</div>

			</view>


			<view style="height:50px">
				<!-- placeholder -->
			</view>
		</view>


	</view>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { globalProps } from '@/js/global.js'
import CardCom from '@/components/CardCom.vue'
import { onReachBottom } from '@dcloudio/uni-app';


const statusBarHeight = ref(globalProps.statusBarHeight)
const capsuleHeight = ref(globalProps.capsuleHeight)

// 列表分页
const pageNum = ref(1)
const pageSize = ref(5)
const listTotal = ref(100)


onMounted(() => {
	console.log('mounted')
	getRedoList()
})

// 获取巩固历史列表
const getRedoList = () => {
	uni.request({
		url: globalProps.baseApi + '/redoRecord',
		method: 'GET',
		header: {
			'Authorization': 'Bearer ' + globalProps.token
		},
		data: {
			pageNum: pageNum.value,
			pageSize: pageSize.value,
			stuID: globalProps.userInfo.id
		},
		success: (res) => {
			console.log('获取题目列表：', res.data)
			// 为题目列表赋值
			currentRedoList.value = currentRedoList.value.concat(res.data.records)
			// 为总页数赋值
			listTotal.value = res.data.total
			if(res.data.records.length === 0){
				uni.showToast({
					title: '没有更多了',
					icon: 'none'
				})
			}
		},
		fail: (err) => {
			uni.showToast({
				title: '获取题目列表失败',
				icon: 'none'
			})
			console.log(err)
		}
	})
}

onReachBottom(() => {
	console.log('到底了')
	if (pageNum.value * pageSize.value < listTotal.value) {
		pageNum.value++
		getRedoList()
	}else{
		uni.showToast({
			title: '没有更多了',
			icon: 'none'
		})
	}
})

// 跳转到个性化练习页面，新版已砍掉
// const navigateToPage = () => {
// 	uni.navigateTo({
// 		url: '/pages/HomePage/GenExercisesPage'
// 	});
// }

// 获取所有错题并跳转到遗忘曲线页面
const getAllRedoThenJump = () => {
	let getUrl = globalProps.baseApi + 'cuotiji/cuotiForRedo/?userID=' + globalProps.userInfo.id
	uni.request({
		url: getUrl,
		method: 'GET',
		header: {
			'Authorization': 'Bearer ' + globalProps.token
		},
		success: (res) => {
			console.log('成功生成练习：', res.data)
			uni.setStorageSync('exerciseList', res.data);
			allRedoJump()
		},
		fail: (err) => {
			uni.showToast({
				title: '生成练习失败',
				icon: 'none'
			})
			console.log(err)
		}
	})

}

// 不过滤条件的直接跳转
const allRedoJump = () => {
	console.log('allRedoJump()')
	uni.navigateTo({
		url: '/pages/AIConsolidationPage/QuestionShowPage',
		success: (res) => {
			console.log('跳转成功', res);
		}
	});
}

// 翻页 代办
const handleChange = () => {
	console.log('翻页', pageNum.value)
	getRedoList()
}

// 跳转到题目详情页
const redoHistoryJump = (cuotiId, redoId, category, item) => {
	// 将当前题目存入缓存
	uni.setStorageSync('redoItem', item)
	uni.navigateTo({
		url: '/pages/AIConsolidationPage/RedoDetailPage?id=' + cuotiId + '&redoId=' + redoId + '&category=' + category
	});
}

// 滚动区域
const loaded = ref(true)
const currentRedoList = ref([])

</script>

<style>
@import "@/css/global.css";
@import "@/css/animation.css";

.aistudy-pg-container {
	/* background-color: gray; */
	margin: 15px 20px;
}


.entries {
	position: fixed;
	bottom: 0;
	right: 0;
	display: flex;
	align-items: center;
	justify-content: space-between;
	flex: 1;
	margin: 15px 20px;
}

.aistudy-pg-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	font-size: larger;
	font-weight: bold;
	/* height: 60px; */
	padding: 15px;
	border-radius: 50%;
	background: rgb(0, 71, 202);
	box-shadow: 0 0px 10px rgba(0, 0, 0, 0.1);
	width: calc(100%)
}

.scroll-container {
	margin-top: 15px;
	flex: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	overflow-x: hidden;
	overflow-y: scroll;
	position: relative;
	animation: bottom-in-ani .8s 1;
}

.ques-line {
	width: calc(100%);
	height: 104px;
	margin: 10px 0;
	border-radius: 12px;
	color: #fff;
	display: flex;
	flex-direction: column;
	white-space: nowrap;
	justify-content: center;
}

.ques-line-line {
	display: flex;
	margin: 3px 0;
	align-items: center;
}

.ques-line-line .ques-header {
	font-weight: bold;
	letter-spacing: 2px;
	font-size: 17px;
	width: calc(100% - 100px);
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.ques-line-line .ques-time {
	font-size: 11px;
}

.line-line-display {
	font-size: 12px;
	color: #ddd;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.ques-line-line .tag {
	background-color: #4942ad;
	padding: 4px 8px;
	font-size: 13px;
	margin-right: 8px;
	border-radius: 4px;
	margin-left: -2px;
}

.tag {
	display: inline-block;
	width: fit-content;
	box-sizing: content-box;
	border-radius: 10px;
	background-color: rgb(77, 74, 223);
	padding: 2px 8px;
}

.redoItem {
	background: linear-gradient(to right bottom, #1c3364, #19035b);
	border-radius: 8px;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	padding: 16px;
	margin-bottom: 16px;
}

/* .redoItem .tag {
  color: #fff;
  font-weight: bold;
  background-color: rgb(77, 74, 223);
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
} */

.redoItem .question-self {
	font-size: 16px;
	font-weight: bold;
	margin-bottom: 12px;
	max-height: 100px;
	overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.redoItem .choice {
	margin-bottom: 8px;
}

.redoItem .false-reason {
	background-color: #ff4d4f;
	display: inline-block;
	width: fit-content;
	box-sizing: content-box;
	border-radius: 10px;
	padding: 2px 8px;
}

.item-head {
	display: flex;
	justify-content: space-between;
	margin-bottom: 20rpx;
}
</style>
