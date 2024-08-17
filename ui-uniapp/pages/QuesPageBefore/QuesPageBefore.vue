<template>
	<wd-config-provider theme="dark">
		<view class="tabbarpage-container">
			<!--胶囊上方-->
			<div :style="{'padding-top': statusBarHeight}">

			</div>
			<!--胶囊-->
			<div class="head-container" :style="{'height': capsuleHeight}">
				错题本
			</div>
			<!--主体-->
			<div class="tabbarpage-body flex-column">
				<!--日期查询-->
				<div class="calendar-container">
					<div class="h1" style="margin-bottom: 0;">日期选择</div>
					<div style="width: calc(100% - 100px);">
						<wd-calendar type="daterange" v-model="dateRange" @confirm="handleDateConfirm" />
					</div>
				</div>
				<!--全部错题-->
				<div class="top-container" style="display: flex; flex-direction: row;">
					<div class="all-ques-btn" @click="pageJump(9, 0)" style="flex-grow: 2">
						<div class="h11">全部错题</div>
						<div class="img-container">
							<img style="width: 14vw;"
								src="https://www.yym-free.com/resource/default/png/78cb9707-b46e-4b5f-8911-2a06be6a69db.png"
								mode="aspectFit" />
						</div>
					</div>
					<!--智能巩固-->
					<div class="all-ques-btn" @click="jumpAiConsolidation" style="flex-grow: 0.5; padding: 0 8px;">
						<div class="h11">智能巩固</div>
					</div>
				</div>



				<!--智能分类-->
				<div class="bottom-container">
					<div class="h1">智能分类</div>
					<div class="line">
						<div class="h2-container">
							<div class="h2">题型</div>
							<div style="width: calc(100% - 120px);">
								<wd-search hide-cancel />
							</div>
						</div>
						<div class="scroll-container">
							<div @click="pageJump(1, item.value)" class="folder-container"
								v-for="(item, index) in bottomList.tixing">
								<img style="height: 48px;" mode="heightFix"
									src="https://www.yym-free.com/resource/default/png/46731167-c292-4e4b-acdd-ca19925adb90.png"
									alt="" />
								<div>{{item.label}}</div>
							</div>
						</div>
					</div>
					<div class="line">
						<div class="h2-container">
							<div class="h2">易错点</div>
							<div style="width: calc(100% - 120px);">
								<wd-search hide-cancel />
							</div>
						</div>
						<div class="scroll-container">
							<div @click="pageJump(0, item.value)" class="folder-container"
								v-for="(item, index) in bottomList.yicuo">
								<img style="height: 48px;" mode="heightFix"
									src="https://www.yym-free.com/resource/default/png/46731167-c292-4e4b-acdd-ca19925adb90.png"
									alt="" />
								<div>{{item.label}}</div>
							</div>
						</div>
					</div>
					<div class="line">
						<div class="h2-container">
							<div class="h2">领域</div>
							<div style="width: calc(100% - 120px);">
								<wd-search hide-cancel />
							</div>
						</div>
						<div class="scroll-container">
							<div @click="pageJump(2, item.value)" class="folder-container"
								v-for="(item, index) in bottomList.lingyu">
								<img style="height: 48px;" mode="heightFix"
									src="https://www.yym-free.com/resource/default/png/46731167-c292-4e4b-acdd-ca19925adb90.png"
									alt="" />
								<div>{{item.label}}</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<!--Tabbar-->
			<TabbarCom :tabbarIndex="1" class="tabbarpage-tabbar" />
		</view>
	</wd-config-provider>
</template>

<script setup>
	import TabbarCom from '@/components/TabbarCom.vue'
	import { onBeforeMount, onMounted, ref } from 'vue';
	import { globalProps } from '@/js/global.js'
	import { tagsPostToTags } from '@/js/apiJsHelper.js'
	
	const statusBarHeight = ref(globalProps.statusBarHeight)
	const capsuleHeight = ref(globalProps.capsuleHeight)
	onBeforeMount(()=>{
		uni.hideTabBar({
			animation: false
		})
		initGetData();
	})
	
	//获取数据
	const initGetData = ()=>{
		uni.request({
		  url: globalProps.baseApi + 'cuotiji/tagByTime',
		  method: 'GET',
		  data:{
			  userID: globalProps.userInfo.id
		  },
		  success: function (res) {
		    console.log('请求成功', res.data);
		    bottomList.value = tagsPostToTags(res.data)
		  },
		  fail: function (err) {
		    console.log('请求失败', err);
		    uni.showToast({
		    	title: '获取纠错数量失败',
				icon: 'error'
		    })
		  }
		});
	}
	onMounted(()=>{
		//初始化Unix时间
		var currentDate = new Date();
		var unixTime = currentDate.getTime();
		dateRange.value[1] = unixTime;
	})
	
	//智能分类
	const searchProps = ref({
		yicuo:null,
		tixing: null,
		lingyu: null,
	})
	const search = ()=>{
		console.log('aaa')
	}
	const bottomList = ref({
		yicuo:[],
		tixing:[],
		lingyu:[]
	})
	//分类查询
	const pageJump = (mode, value)=>{
		let jumpProps = {
			dateRange: dateRange.value,
			tagList: JSON.parse(JSON.stringify(bottomList.value)),
			userID: globalProps.userInfo.id,
			order: 'DESC',
			specialCategory: null
		}
		if(mode === 0){
			//易错点
			jumpProps.tagList.yicuo = [{label:null, value:value}]
		}else if(mode === 1){
			//题型
			jumpProps.specialCategory = value
		}else if(mode === 2){
			//领域
			jumpProps.tagList.lingyu = [{label:null, value:value}]
		}
		//页面跳转
		uni.navigateTo({
			url: '/pages/QuesPage/QuesPage?props='+JSON.stringify(jumpProps)
		})
	}
	
	//日期查询
	const dateRange = ref({
		0: 0,
		1: 0
	})
	const handleDateConfirm = ()=>{
		console.log(dateRange.value)
	}

	// 智能巩固
	const jumpAiConsolidation = ()=>{
		uni.navigateTo({
			url: '/pages/ReviewPage/ReviewDetail/ReviewDetail',
		});
	}
	
</script>

<style>
	@import "@/css/global.css";
	@import "@/css/animation.css";
	.head-container{
		display: flex;
		align-items: center;
		margin: 0 16px;
		justify-content: center;
		color: #fff;
		width: calc(100% - 32px);
		letter-spacing: 1px;
	}
	.flex-column{
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
	}
	/*全部错题*/
	.top-container{
		width: calc(100% - 28px);
		height: 130px;
		color: #fff;
		padding: 12px 8px 0 8px;
		white-space: pre-line;
		word-break: break-all;
		display: flex;
		flex-direction: column;
		animation: top-in-ani .8s 1;
	}
	.top-container .all-ques-btn{
		height: 100px;
		background: linear-gradient(to right bottom, #375cac, #3b1a9d);
		border-radius: 8px;
		margin: 4px 8px;
		display: flex;
		position: relative;
		justify-content: center;
		align-items: center;
	}
	.all-ques-btn .img-container{
		width: 14vw;
		height: 14vw;
		display: flex;
		align-items: center;
		justify-content: center;
		transform: rotateZ(-15deg);
		animation: book-ani 1.6s 1;
	}
	@keyframes book-ani {
		0%{
			transform: rotateZ(-15deg) translateX(100%);
		}
	}
	.all-ques-btn .h11{
		font-size: 21px;
		font-weight: bold;
		letter-spacing: 2px;
		animation: text-ani 1.2s 1;
	}
	/*智能分类*/
	.bottom-container{
		flex: 1;
		width: calc(100% - 28px);
		margin: 8px 4px 4px 4px;
		color: #fff;
		padding: 0 8px 0 8px;
		white-space: pre-line;
		word-break: break-all;
		display: flex;
		flex-direction: column;
		animation: bottom-in-ani .8s 1;
	}
	.bottom-container .line{
		flex: 1;
		margin: 0 8px 8px 8px;
		display: flex;
		flex-direction: column;
	}
	.line .h2-container{
		width: 100%;
		height: 40px;
		margin-bottom: 12px;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.line .h2{
		font-size: 16px;
		font-weight: bold;
		letter-spacing: 1px;
	}
	.line .scroll-container{
		flex: 1;
		width: calc(100% - 16px);
		margin-bottom: 4px;
		overflow-y: hidden;
		overflow-x: scroll;
		display: flex;
		background: linear-gradient(to top, #3b1a9daa, #375cac22);
		padding: 0 8px;
		border-radius: 8px;
	}
	.line .scroll-container .folder-container{
		color: white;
		display: flex;
		align-items: center;
		flex-direction: column;
		white-space: nowrap;
		margin: 0 12px;
		font-size: 13px;
	}
	.h1{
		font-weight: bold;
		letter-spacing: 1px;
		font-size: 18px;
		margin-bottom: 12px;
	}
	:deep(.wd-search){
		background: transparent !important;
	}
	/*日历查询*/
	.calendar-container{
		height: 40px;
		align-items: center;
		justify-content: space-between;
		width: calc(100% - 28px);
		margin: 8px 4px 4px 4px;
		color: #fff;
		padding: 0 8px 0 8px;
		white-space: pre-line;
		word-break: break-all;
		display: flex;
		animation: bottom-in-ani .8s 1;
		padding-bottom: 4px;
	}
	
	
</style>
