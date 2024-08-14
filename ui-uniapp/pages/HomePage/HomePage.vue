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
		<div style="height:15px"></div>
		<TabbarCom :tabbarIndex="0" class="tabbarpage-tabbar" />
	</view>
	
</template>

<script setup>
	import { onBeforeMount, ref } from 'vue';
	import { globalProps } from '@/js/global.js'
	import NewUICom from './components/NewUICom.vue';
	import TabbarCom from '@/components/TabbarCom.vue';
	

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
