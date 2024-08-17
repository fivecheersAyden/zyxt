<template>
	<wd-config-provider theme="dark">
		<view class="tabbarpage-container">
			<!--胶囊上方-->
			<div :style="{'padding-top': statusBarHeight}">
				
			</div>
			<!--胶囊-->
			<div class="head-container" :style="{'height': capsuleHeight}">
				<wd-icon @click="jumpBack" color="#fff" name="thin-arrow-left" size="18px"></wd-icon>
				<div>错题本</div>
				<div style="width: 18px;"></div>
			</div>
			<!--主体-->
			<div class="tabbarpage-body">
				<div class="body-content">
					<!--选择器-->
					<div class="select-container">
						<div @click="changeTimeSelect" class="time-select" v-if="latest">排序<wd-icon name="arrow-thin-down" size="13px"></wd-icon></div>
						<div @click="changeTimeSelect" class="time-select" v-if="!latest">排序<wd-icon name="arrow-thin-up" size="13px"></wd-icon></div>
						<div class="picker-container">
							<wd-select-picker @confirm="selectCategory" z-index="999" label="类型" v-model="quesType" :columns="quesTypeColumns" filterable></wd-select-picker>
						</div>
					</div>
					<!--滑动-->
					<div class="scroll-container">
						<div v-if="loaded" @click="quesPageJump(item.quesId)" class="ques-line dark-purple-card" v-for="item in currentQuesList" :key="item.quesId">
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
								{{item.quesDisplay}}
							</div>
						</div>
						<div v-for="i in 5" style="height: 100%; justify-content: space-around; padding: 12px;" class="ques-line dark-purple-card" v-else>
							<wd-skeleton theme="paragraph" />
						</div>
						<div @click="searchAppend" class="more-btn">- 更多 -</div>
					</div>
				</div>
				<!--底部tabbar占据高度72px-->
			</div>
		</view>
	</wd-config-provider>
</template>

<script setup>

	import { onBeforeMount, ref, reactive, onMounted } from 'vue';
	import { globalProps } from '@/js/global.js'
	import { onLoad, onShow } from '@dcloudio/uni-app'
	import timestampToFormattedDateTime from '@/js/timestampToFormattedDateTime.js'
	
	const statusBarHeight = ref(globalProps.statusBarHeight)
	const capsuleHeight = ref(globalProps.capsuleHeight)
	
	const jumpBack = ()=>{
		uni.navigateBack()
	}
	
	//选择区域
	const latest = ref(true)
	const changeTimeSelect = ()=>{
		latest.value = !latest.value
		clearList()
		searchAppend()
	}
	
	onLoad((e)=>{
		//初始化查询条件并查询
		const loadProps = JSON.parse(e.props)
		console.log(loadProps)
		timeRange.value = loadProps.dateRange
		userID.value = loadProps.userID
		order.value = loadProps.order
		fieldList.value = loadProps.tagList.lingyu
		falseReasonList.value = loadProps.tagList.yicuo
		quesTypeColumns.value = loadProps.tagList.tixing
		if(loadProps.specialCategory !== null){
			//单独某种题型
			quesType.value = [loadProps.specialCategory]
		}else{
			for (let t of loadProps.tagList.tixing) {
				quesType.value.push(t.value)
			}
		}
	})
	onShow(()=>{
		clearList()
		searchAppend()
	})
	//查询条件
	const timeRange = ref({
		0: 0,
		1: 0
	})
	const userID = ref('1')
	const order = ref('DESC')
	const fieldList = ref([])
	const falseReasonList = ref([])
	const quesType = ref([])
	const quesTypeColumns = ref([])
	const quesListParams = ref({
		firstIndex: 0,
		searchLength: 10
	})
	
	//查询
	const searchAppend = ()=>{
		let getUrl = 'http://localhost:7349/cuotiji/v2?' + 
						'userID=' + userID.value +
						'&order=' + order.value + 
						'&pageNum=' + quesListParams.value.firstIndex + 
						'&pageSize=' + quesListParams.value.searchLength
		for (let qt of quesType.value) {
			getUrl += '&category=' + qt
		}
		for (let fr of falseReasonList.value) {
			getUrl += '&falseReason=' + fr.value
		}
		for (let f of fieldList.value) {
			getUrl += '&field=' + f.value
		}
		console.log('查询URL: ' + getUrl)
		
		uni.request({
		  url: getUrl,
		  method: 'GET',
		  success: function (res) {
		    console.log('请求成功', res.data);
			if(res.data.records.length > 0){
				for (let ques of res.data.records) {
					let newQues = {
						quesId: ques.id,
						addTime: timestampToFormattedDateTime(ques.insertTime),
						quesRemark: ques.userComment,
						tags:[ques.category === 'zuowen' ? '作文' : ques.category === 'yuedu' ? '阅读' : ques.category === 'fanyi' ? '翻译' : ques.category === 'xuanze' ? '选择' : '未知类型', ques.falseReason, ques.field === null ? '其他领域' : ques.field],
						quesDisplay: ques.content
					}
					currentQuesList.value.push(newQues)
				}
				quesListParams.value.firstIndex += quesListParams.value.searchLength
			}else{
				uni.showToast({
					title: '后面没有了',
					icon: 'none'
				})
			}
		  },
		  fail: function (err) {
		    console.log('请求失败', err);
		    uni.showToast({
		    	title: '获取错题失败',
				icon: 'error'
		    })
		  }
		});
	}
	
	//清空列表
	const clearList = ()=>{
		currentQuesList.value = []
		quesListParams.value.firstIndex = 0
		quesListParams.value.searchLength = 10
	}
	
	//滚动区域
	const loaded = ref(true)
	const currentQuesList = ref([])
	const quesPageJump = (quesId)=>{
		uni.request({
		  url: 'http://localhost:7349/cuotiji/detail?userID=' + userID.value + '&cuotiID=' + quesId,
		  method: 'GET',
		  success: function (res) {
		    console.log('请求成功', res.data);
			if(res.data.category === "yuedu" || res.data.category === 'xuanze'){
				uni.navigateTo({
					url: '/pages/manageques/ManagePassageQuesPage/ManagePassageQuesPage?jsonData=' + encodeURIComponent(JSON.stringify(res.data))
				})
			}else if(res.data.category === "zuowen" || res.data.category === "fanyi"){
				
				uni.navigateTo({
					url: '/pages/manageques/ManageQuesPage/ManageQuesPage?jsonData=' + encodeURIComponent(JSON.stringify(res.data))
				})
			}
		  },
		  fail: function (err) {
		    console.log('请求失败', err);
		    uni.showToast({
		    	title: '获取错题失败',
				icon: 'error'
		    })
		  }
		});
		/* uni.navigateTo({
		  url: '/pages/QuesDeepPage/QuesDeepPage?quesId='+quesId
		}) */
	}
	const selectCategory = ()=>{
		clearList()
		searchAppend()
	}
	
	
</script>

<style>
	@import "@/css/global.css";
	@import "@/css/animation.css";
	@import "@/css/quesselect.css";
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
	.body-content .select-container{
		height: 32px;
		width: calc(100% - 24px);
		margin: 16px 12px 8px 12px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		color: #fff;
		letter-spacing: 1px;
		animation: top-in-ani .6s 1;
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
		height: 112px;
		margin: 10px 0;
		border-radius: 12px;
		color: #fff;
		display: flex;
		flex-direction: column;
		white-space: nowrap;
		justify-content: center;
		padding: 0 12px;
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
	}
	.line-line-display{
		font-size: 12px;
		color: #ddd;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.ques-line-line .tag{
		background-color: #4942ad;
		padding: 4px 8px;
		font-size: 13px;
		margin-right: 8px;
		border-radius: 4px;
		margin-left: -2px;
	}
	.more-btn{
		color: #ddd;
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
