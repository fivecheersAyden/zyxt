<template>
	<view class="tabbarpage-container">
		<view class="status_bar">
		    <!-- 这里是状态栏 -->
		</view>
		<!-- <view class="page-header" :style="{'height': '35px'}">
			小英老师
		</view> -->
		<!--主体-->
		<view class="tabbarpage-body">
			<view class="absolute-all-container">
				<NewUICom class="absolute-all-container"/>
			</view>
		</view>
		<TabbarCom :tabbarIndex="0" class="tabbarpage-tabbar" />
		<!-- <button style="position: fixed; top: 50%; left: 50%;" @click="aaa">aaa</button> -->
	</view>
	
</template>

<script setup>
	import { onBeforeMount, onMounted, ref } from 'vue';
	import { globalProps } from '@/js/global.js'
	import NewUICom from './components/NewUICom.vue';
	import TabbarCom from '@/components/TabbarCom.vue';
	
	// const aaa = ()=>{
	// 	console.log('aaa')
	// 	let innerAudioContext = uni.createInnerAudioContext();
	// 	innerAudioContext.obeyMuteSwitch = false
	// 	// console.log('音频播放源','https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts?appkey=' + that.myAppkey + '&speech_rate=' + that.speech_rate + '&voice=' + that.voice + '&token=' + res.data + '&text=' + encodeText + `&format=wav&sample_rate=16000`)
	// 	innerAudioContext.src = 'https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts?appkey=2hfVbAU7ahbvM4a2&speech_rate=144&voice=zhixiaoxia&token=db4b1cfd79d649a4897547be6f8d9230&text=%E4%BD%A0%E5%A5%BD%EF%BC%81%E5%BE%88%E9%AB%98%E5%85%B4&format=wav&sample_rate=16000';
	// 	innerAudioContext.play();
	// }
	

</script>

<style>
	@import "@/css/global.css";
	@import "@/css/animation.css";
	
	.absolute-all-container{
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		top: 0;
	}
	page{
		color: white;
	}
	
	
</style>
