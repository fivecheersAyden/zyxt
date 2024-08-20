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
				历史对话
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<div class="body-content">
				<!--搜索框-->
				<div class="search-container">
					<wd-search @change="changeSearch" @search="search" hide-cancel style="width: 100%;"/>
				</div>
				<!--选择器-->
				<div class="select-container">
					<div @click="changeTimeSelect" class="time-select" v-if="latest">排序<wd-icon name="arrow-thin-down" size="13px"></wd-icon></div>
					<div @click="changeTimeSelect" class="time-select" v-if="!latest">排序<wd-icon name="arrow-thin-up" size="13px"></wd-icon></div>
					<div style="width: calc(100% - 100px); border-radius: 8px; overflow: hidden;">
						<wd-calendar type="daterange" v-model="dateRange" @confirm="handleDateConfirm" />
					</div>
				</div>
				<!--滑动-->
				<div class="scroll-container">
					<div @click="quesPageJump(item.id)" class="ques-line" v-for="item in currentQuesList" :key="item.id">
						<div style="justify-content: space-between;" class="ques-line-line">
							<div class="ques-time">{{ item.questime }}</div>
						</div>
						<div class="ques-line-line line-line-display">
							{{item.summary}}
						</div>
						<div class="ques-line-line" style="overflow-x: scroll;">
							<div class="tag" v-for="tag in item.knowledge">
								{{ tag }}
							</div>
						</div>
					</div>
					<div @click="searchAppend" class="more-btn">- 更多 -</div>
				</div>
			</div>
		</view>
	</view>
</template>

<script setup>
	import timestampToFormattedDateTime from '@/js/timestampToFormattedDateTime.js'
	import { globalProps } from '@/js/global.js';
	import { onMounted, ref } from 'vue';
	import TabbarCom from '@/components/TabbarCom.vue';
	
	//当前习题
	const currentQuesList = ref([])
	//knowledge处理
	const knowledge = ref(null)
	const changeSearch = (e)=>{
		knowledge.value = e.value
	}
	//日期处理
	onMounted(()=>{
		//初始化Unix时间
		var currentDate = new Date();
		var unixTime = currentDate.getTime();
		dateRange.value[1] = unixTime;
		dateRange.value[0] = 1713974400000
		//获取用户id并查询习题数量
		getId()
	})
	const dateRange = ref({
		0: 0,
		1: 0
	})
	const handleDateConfirm = ()=>{
		pageParams.value.startIndex = 1
		currentQuesList.value = []
		searchAppend()
	}
	//排序处理
	const latest = ref(true)
	const changeTimeSelect = ()=>{
		latest.value = !latest.value
		pageParams.value.startIndex = 1
		currentQuesList.value = []
		searchAppend()
	}
	//页码处理
	const pageParams = ref({
		startIndex: 1,
		length: 10
	})
	//id，token处理
	const id = ref()
	const token = ref()
	const getId = ()=>{
		uni.getStorage({
			key: 'loginStorage',
			success(res) {
				id.value = res.data.userInfo.id
				token.value = res.data.token
				//首次查询
				searchAppend()
			}
		})
	}
	
	//查询
	const searchAppend = ()=>{
		uni.request({
			url: globalProps.baseApi + 'question',
			method: 'GET',
			header: {
			        'Authorization': 'Bearer ' + token.value
			},
			data:{
				knowledge: null,
				orderType: latest.value ? 'DESC' : 'ASC', // 排序类型
				pageNum: pageParams.value.startIndex, // 页码
				pageSize: pageParams.value.length, // 每页大小
				studentID: id.value, // 学生ID
				minTime: timestampToFormattedDateTime(dateRange.value[0]), // 最小时间
				maxTime: timestampToFormattedDateTime(dateRange.value[1]) // 最大时间
			},
			success(res) {
				console.log('查询习题返回结果',res)
				if(res.data.records.length <= 0){
					uni.showToast({
						icon: 'none',
						title: '后面没有了'
					})
					return
				}
				for (let record of res.data.records) {
					record.knowledge = record.knowledge.split(/[,\s]+/);
					currentQuesList.value.push(record)
				}
				pageParams.value.startIndex += pageParams.value.length
			},
			fail(e) {
				uni.showToast({
					icon: 'error',
					title: '查询失败'
				})
				console.log('查询习题失败',e)
			}
		})
	}
	const search = ()=>{
		console.log(knowledge.value)
		pageParams.value.startIndex = 1
		currentQuesList.value = []
		uni.request({
			url: globalProps.baseApi + 'question',
			method: 'GET',
			header: {
			        'Authorization': 'Bearer ' + token.value
			},
			data:{
				knowledge: knowledge.value,
				orderType: latest.value ? 'DESC' : 'ASC', // 排序类型
				pageNum: pageParams.value.startIndex, // 页码
				pageSize: pageParams.value.length, // 每页大小
				studentID: id.value, // 学生ID
				minTime: timestampToFormattedDateTime(dateRange.value[0]), // 最小时间
				maxTime: timestampToFormattedDateTime(dateRange.value[1]) // 最大时间
			},
			success(res) {
				console.log('查询习题返回结果',res)
				if(res.data.records.length <= 0){
					uni.showToast({
						icon: 'none',
						title: '没有结果'
					})
					return
				}
				for (let record of res.data.records) {
					record.knowledge = record.knowledge.split(/[,\s]+/);
					currentQuesList.value.push(record)
				}
				pageParams.value.startIndex += pageParams.value.length
			},
			fail(e) {
				uni.showToast({
					icon: 'error',
					title: '查询失败'
				})
				console.log('查询习题失败',e)
			}
		})
	}
	
	//页面跳转
	const quesPageJump = (questionID)=>{
		uni.navigateTo({
			url: '/pages/HistoryDialagueDetail/HistoryDialagueDetail?questionID=' + questionID + '&stuID=' + id.value + '&token=' + token.value
		})
	}
	
</script>

<style>
	@import url("@/css/global.css");
	@import url("@/css/animation.css");
	.head-container{
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		letter-spacing: 1px;
	}
	.body-content{
		position: absolute;
		top: 0;
		bottom: 12px;
		left: 0;
		right: 0;
		display: flex;
		flex-direction: column;
	}
	.body-content .search-container{
		height: 48px;
		width: 100%;
		display: flex;
		align-items: center;
		animation: top-in-ani 1 .6s;
	}
	.search-container :deep(.wd-search){
		background-color: transparent !important; 
	}
	.search-container :deep(.wd-search__cover){
		background-color: #fdfdfd !important;
	}
	.body-content .select-container{
		height: 32px;
		width: calc(100% - 24px);
		margin: 16px 12px 16px 12px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		color: #fff;
		letter-spacing: 1px;
		animation: top-in-ani .6s 1;
	}
	.body-content .select-container .time-select{
		/* color: #333; */
	}
	.body-content .scroll-container{
		margin: 8px;
		width: calc(100% - 16px);
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		overflow-x: hidden;
		overflow-y: scroll;
		position: relative;
		animation: bottom-in-ani .8s 1;
	}
	.ques-line{
		width: calc(100% - 36px);
		margin: 4px 0;
		border-radius: 12px;
		color: #333;
		display: flex;
		flex-direction: column;
		white-space: nowrap;
		justify-content: center;
		padding: 8px 12px;
		background-color: #ffffffee;
		backdrop-filter: blur(8px);
		border: 1px solid #eee;
		box-shadow: 2px 2px 6px #00000011;
	}
	.ques-line-line{
		display: flex;
		margin: 6px 0;
		align-items: center;
	}
	.ques-line-line .ques-header{
		font-weight: bold;
		letter-spacing: 2px;
		font-size: 17px;
		width: calc(100% - 120px);
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.ques-line-line .ques-time{
		font-size: 11px;
		color: #666;
	}
	.line-line-display{
		font-size: 12px;
		color: #333;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: pre-line;
	}
	.ques-line-line .tag{
		background-color: #496cf1;
		color: #fff;
		padding: 4px 8px;
		font-size: 13px;
		margin-right: 8px;
		border-radius: 4px;
		
	}
	.more-btn{
		color: #666;
	}
	.head-container{
		display: flex;
		align-items: center;
		margin: 0 16px;
		justify-content: space-between;
		color: #fff;
		width: calc(100% - 32px);
		letter-spacing: 1px;
	}

</style>
