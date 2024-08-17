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
				学情分析
			</view>
			<!-- <view style="width: 18px">
				placeholder for symmetry
			</view> -->
		</view>

		<!--主体-->
		<view class="tabbarpage-body scrollable">
			<view class="growpage-container">
				<RadarChartEvalCom ref="radarDimensionRef" />
				<view style="height:20px">
					<!-- manual padding -->
				</view>
				<LineChartCom ref="lineRef" />
			</view>
		</view>
		<TabbarCom :tabbarIndex="3" class="tabbarpage-tabbar" />
	</view>
</template>

<script setup>
import {
	onBeforeMount,
	ref,
	onMounted,
	watch
} from 'vue';
import {
	globalProps
} from '@/js/global.js'
import LineChartCom from './components/LineChartCom.vue';
import RadarChartEvalCom from '@/pages/GrowPage/components/RadarChartEvalCom.vue';
import TabbarCom from '@/components/TabbarCom.vue';

onBeforeMount(() => {
	uni.hideTabBar({
		animation: false
	})
})

onMounted(() => {
	getGrowData()
})

const radarQuesTypeRef = ref(null)
const radarDimensionRef = ref(null)
const lineRef = ref(null)

const getGrowData = () => {
	let jsonObj = null;
	uni.request({
		url: globalProps.baseApi + 'levelRecord/detail',
		method: 'GET',
		header: {
			'Authorization': 'Bearer ' + globalProps.token
		},
		data: {
			stuID: globalProps.userInfo.id
		},
		success: function (res) {
			console.log('请求成功', res.data);
			backendData.value = res.data
			// backendData.value = backendDataFake.value
			// 调用转格式函数
			jsonObj = JSON.parse(JSON.stringify(frontendFormat(backendData.value)));
			if (radarQuesTypeRef.value) {
				radarQuesTypeRef.value.showData(jsonObj.questionTypeCorrectRate)
			} else {
				console.log('雷达图题型组件未加载')
			}
			if (radarDimensionRef.value) {
				radarDimensionRef.value.showData(jsonObj.abilityDimension)
			} else {
				console.log('雷达图能力维度组件未加载')
			}
			if (lineRef.value) {
				lineRef.value.showData(jsonObj.overallPerformanceWithTime)
			} else {
				console.log('折线图组件未加载')
			}
		},
		fail: function (err) {
			console.log('请求失败', err);
			uni.showToast({
				title: '获取学情分析失败',
				icon: 'error'
			})
		}
	});
}

const backendDataFake = ref({
	"id": null,
	"startTimeStr": null,
	"endTimeStr": null,
	"startTime": null,
	"endTime": null,
	"overlevel": 0,
	"overEvaluation": null,
	"stuID": 0,
	"lanCompreScore": null,
	"lanCompreComment": null,
	"lanExpreScore": null,
	"lanExpreComment": null,
	"lanKnowledgeScore": null,
	"lanKnowledgeComment": null,
	"choicePerformance": null,
	"choiceSuggestion": null,
	"readingPerformance": null,
	"readingSuggestion": null,
	"essayPerformance": null,
	"essaySuggestion": null,
	"overLevels": [
		0,
		0,
		0,
		6.5,
		0
	],
	"suggestions": [
		null,
		null,
		null,
		"该学生在选择题和阅读理解方面表现一般，需要加强审题和细节理解能力；在翻译和作文方面表现较好，但仍有提升空间。建议学生多加练习选择题和阅读理解，注重细节理解；同时在翻译和写作中提高语法准确性和语言表达能力。综合来看，学生有一定潜力，但需要更多努力和指导才能取得更好的成绩。",
		null
	],
	"correctRate": [],
	"translationSuggestion": null,
	"translationPerformance": null
})

const backendData = ref({});

const frontendFormat = (backendData) => {
	console.log('转格式时打印后端数据: ', backendData);
	if(backendData.lanCompreComment === null) {
		backendData.lanCompreScore = 0
		backendData.lanCompreComment = '暂无评价，多多使用本系统练习吧！'
		backendData.lanExpreScore = 0
		backendData.lanExpreComment = '暂无评价，多多使用本系统练习吧！'
		backendData.lanKnowledgeScore = 0
		backendData.lanKnowledgeComment = '暂无评价，多多使用本系统练习吧！'
	}
	return {
		"overallPerformanceWithTime": {
			"lineData": backendData.overLevels,
			"suggestions": backendData.suggestions
		},
		"abilityDimension": {
			"abilityDimensionData": [
				backendData.lanCompreScore,
				backendData.lanExpreScore,
				backendData.lanKnowledgeScore
			],
			"abilityDimensionDetail": [
				backendData.lanCompreComment,
				backendData.lanExpreComment,
				backendData.lanKnowledgeComment
			]
		},
		"questionTypeCorrectRate": {
			"correctRateData": backendData.correctRate,
			"correctRateDetail": [{
				"question_type": "Choice Questions",
				"performance": backendData.choicePerformance,
				"suggestions": backendData.choiceSuggestion
			},
			{
				"question_type": "Reading Comprehension",
				"performance": backendData.readingPerformance,
				"suggestions": backendData.readingSuggestion
			},
			{
				"question_type": "Translation",
				"performance": backendData.translationPerformance,
				"suggestions": backendData.translationSuggestion
			},
			{
				"question_type": "Essay",
				"performance": backendData.essayPerformance,
				"suggestions": backendData.essaySuggestion
			}
			]
		}
	}
};

</script>

<script>
// export default {
// 	onPullDownRefresh() {
// 		console.log('refresh');
// 		getGrowData()
// 		uni.stopPullDownRefresh();
// 	}
// }
</script>

<style>
@import "@/css/global.css";
@import "@/css/animation.css";

page{
	color: white;
}

.growpage-container {
	margin-top: 15px;
	padding: 0 20px;
	overflow-y: scroll;
}
</style>