<template>
	<wd-tabbar 
		z-index="99" 
		shape="round" 
		v-model="showingTabbarIndex" 
		@change="handleChange" 
		custom-class="custom-tabber" 
		inactive-color="#a6a4b9" 
		active-color="#ffffff"
	>
	  <wd-tabbar-item :value="messageNum[0]" title="主页" icon="home"></wd-tabbar-item>
	  <wd-tabbar-item :value="messageNum[1]" title="错题" icon="list"></wd-tabbar-item>
	  <wd-tabbar-item icon="cart" title="">
	      <template #icon>
	        <wd-img round height="58px" width="58px" src="https://www.yym-free.com/resource/default/png/28ebbe52-773c-4230-a9db-6648a9115ab2.png"></wd-img>
	      </template>
	    </wd-tabbar-item>
	  <wd-tabbar-item :value="messageNum[2]" title="学情" icon="chevron-up-rectangle"></wd-tabbar-item>
	  <wd-tabbar-item :value="messageNum[3]" title="我的" icon="user"></wd-tabbar-item>
	</wd-tabbar>
</template>

<script setup>
	import { onMounted, ref, watch, defineProps } from 'vue';
	import {currentOCR} from '@/js/ques.js'

	const props = defineProps({
		tabbarIndex: Number
	})
	const showingTabbarIndex = props.tabbarIndex
	//消息数量
	const messageNum = ref([0,0,0,0])
	const handleChange = (newIndex)=>{
		switch(newIndex.value){
			case 0:
				uni.switchTab({
					url: '/pages/HomePage/HomePage'
				})
				break;
			case 1:
				uni.switchTab({
					url: '/pages/QuesPageBefore/QuesPageBefore'
				})
				break;
			case 2:
				currentOCR.backToNewQues = true
				uni.navigateTo({
					url: '/pages/newques/CameraPage/CameraPage'
				})
				break;
			case 3:
				uni.switchTab({
					url: '/pages/GrowPage/GrowPage'
				})
				break;
			case 4:
				uni.switchTab({
					url: '/pages/MinePage/MinePage'
				})
				break;
				
		}
	}
</script>

<style>
	
</style>