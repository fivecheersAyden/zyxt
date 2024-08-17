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
		<view class="tabbarpage-body">
			<!--今日复习-->
			<div class="review-container">
				<div class="review-num-container">
					<div>今日剩余复习：</div>
					<div>{{todayQuesList.length}}</div>
					<div>道</div>
				</div>
				<div @click="jumpToReviewDetail" class="review-jump-btn">
					开始复习
				</div>
			</div>
			<!--复习记录-->
			<div class="body-content">
				<!--标题-->
				<wd-divider color="#bbb" style="margin-bottom: 4px;">复习记录</wd-divider>
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
					<div @click="quesPageJump(item.redoID)" class="ques-line" v-for="item in currentQuesList" :key="item.reduID">
						<div style="justify-content: space-between;" class="ques-line-line">
							<div class="ques-time">复习时间：{{ item.redoTime }}</div>
							<div class="ques-time">添加时间：{{ item.insertTime }}</div>
						</div>
						<div class="ques-line-line" >
							<div class="tag">{{ handleCategory(item.category) }}</div>
							<div class="ques-detail" v-if="item.category === 'zuowen' || item.category === 'fanyi' || item.category === 'yuedu'">{{ item.content }}</div>
							<div class="ques-detail" v-else>{{ item.problem }}</div>
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
	import { onShow } from '@dcloudio/uni-app'
	
	onShow(()=>{
		setTimeout(()=>{
			//初始化Unix时间
			initTime()
			//获取用户id
			getId()
		},200)
	})
	
	/**
	 * 复习题目
	 */
	const todayQuesList = ref([])
	const getTodayQuesList = ()=>{
		uni.request({
			url: globalProps.baseApi + 'cuotiji/cuotiForRedo?userID=' + id.value,
			header: {
			        'Authorization': 'Bearer ' + token.value
			},
			success(res) {
				if(res.statusCode === 200){
					todayQuesList.value = res.data
					console.log('查询今日复习题目成功',todayQuesList.value)
				}else{
					uni.showToast({
						icon: 'error',
						title: '查询今日复习失败'
					})
				}
			},
			fail(e) {
				uni.showToast({
					icon: 'error',
					title: '查询今日复习失败'
				})
			}
		})
	}
	const jumpToReviewDetail = ()=>{
		uni.navigateTo({
			url: '/pages/ReviewPage/ReviewDetail/ReviewDetail'
		})
	}
	/**
	 * 温故知新历史
	 */
	//当前习题
	const currentQuesList = ref([])
	//category处理
	const handleCategory = (category)=>{
		let result = null
		switch(category){
			case 'zuowen':
				result = '作文'
				break;
			case 'fanyi':
				result = '翻译'
				break;
			case 'yuedu':
				result = '阅读'
				break;
			case 'xuanze':
				result = '选择'
				break;
		}
		return result
	}
	//knowledge处理
	const knowledge = ref(null)
	const changeSearch = (e)=>{
		knowledge.value = e.value
	}
	//日期处理
	const initTime = ()=>{
		var currentDate = new Date();
		var unixTime = currentDate.getTime();
		dateRange.value[1] = unixTime;
		dateRange.value[0] = 1713974400000
	}
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
				//查询题目
				getTodayQuesList()
			}
		})
	}
	
	//查询
	const searchAppend = ()=>{
		uni.request({
			url: globalProps.baseApi + 'redoRecord',
			method: 'GET',
			header: {
			        'Authorization': 'Bearer ' + token.value
			},
			data:{
				orderType: latest.value ? 'DESC' : 'ASC', // 排序类型
				pageNum: pageParams.value.startIndex, // 页码
				pageSize: pageParams.value.length, // 每页大小
				stuID: id.value, // 学生ID
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
					record.cuoTiList = record.sonExercise
					record.insertTime = timestampToFormattedDateTime(record.insertTime)
					record.redoTime = timestampToFormattedDateTime(record.redoTime)
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
	const quesPageJump = (reduID)=>{
		uni.showToast({
			icon: 'none',
			title: '暂无详情'
		})
	}
	
</script>

<style>
	@import url("@/css/global.css");
	@import url("@/css/animation.css");
	
	/*今日复习*/
	.review-container{
		position: absolute;
		top: 4px;
		right: 12px;
		left: 12px;
		height: 72px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		animation: top-in-ani .6s 1;
	}
	.review-num-container{
		display: flex;
		height: 40px;
		flex: 0.9;
		align-items: flex-end;
	}
	.review-num-container div:nth-child(1),
	.review-num-container div:nth-child(3)
	{
		font-size: 16px;
		letter-spacing: 1px;
		font-weight: bold;
		color: #ffffff;
	}
	.review-num-container div:nth-child(2){
		font-size: 36px;
		margin: 0 12px -6px 4px;
		font-weight: bold;
		color: #790ff1;
	}
	
	.review-jump-btn{
		width: 120px;
		height: 60px;
		background-color: #4942ad;
		color: #fff;
		display: flex;
		align-items: center;
		justify-content: center;
		letter-spacing: 2px;
		font-weight: bold;
		font-size: 17px;
		border-radius: 12px;
		box-shadow: 2px 2px 6px #00000011;
	}
	/*复习历史*/
	.head-container{
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		letter-spacing: 1px;
	}
	.body-content{
		position: absolute;
		top: 88px;
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
		width: calc(100% - 24px);
		margin: 4px 0;
		border-radius: 12px;
		color: #333;
		display: flex;
		flex-direction: column;
		white-space: nowrap;
		justify-content: center;
		padding: 8px 12px;
		background-color: #fff;
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
		padding: 4px 6px;
		font-size: 10px;
		margin-right: 8px;
		border-radius: 4px;
		
	}
	.ques-line-line .ques-detail{
		font-size: 12px;
		overflow: hidden;
		text-overflow: ellipsis;
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
