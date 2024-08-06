<template>
	<div class="xuanze-card">
		<div class="h1">选项：</div>
		<div class="xuanze-line dark-purple-card" :class="{'wrong': answer !== null && stuAnswer === 'A' && answer!== 'A', 'right': answer !== null && stuAnswer === 'A' && answer=== 'A', 'medium': answer === null && stuAnswer === 'A' }" @click="changeStuAnswer('A')">
			<div v-if="mode==='normal'">{{choice1}}</div>
			<input v-else style="width: calc(100% - 80px); padding: 4px 12px; background-color: #ffffff11; z-index: 0;" v-model="choice1"/>
			<!--用户选择错误答案-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'A' && answer!== 'A'" name="close-circle-filled" size="22px"></wd-icon>
			<!--正确-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'A' && answer === 'A'" name="check-circle-filled" size="22px"></wd-icon>
			<!--选择（无答案）-->
			<wd-icon color="#fff" v-if="answer === null && stuAnswer === 'A'" name="info-circle-filled" size="22px"></wd-icon>
		</div>
		<div class="xuanze-line dark-purple-card" :class="{'wrong': answer !== null && stuAnswer === 'B' && answer!== 'B', 'right': answer !== null && stuAnswer === 'B' && answer=== 'B', 'medium': answer === null && stuAnswer === 'B' }" @click="changeStuAnswer('B')">
			<div v-if="mode==='normal'">{{choice2}}</div>
			<input v-else style="width: calc(100% - 80px); padding: 4px 12px; background-color: #ffffff11; z-index: 0;" v-model="choice2"/>
			<!--用户选择错误答案-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'B' && answer !== 'B'" name="close-circle-filled" size="22px"></wd-icon>
			<!--正确-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'B' && answer === 'B'" name="check-circle-filled" size="22px"></wd-icon>
			<!--选择（无答案）-->
			<wd-icon color="#fff" v-if="answer === null && stuAnswer === 'B'" name="info-circle-filled" size="22px"></wd-icon>
		</div>
		<div class="xuanze-line dark-purple-card" :class="{'wrong': answer !== null && stuAnswer === 'C' && answer!== 'C', 'right': answer !== null && stuAnswer === 'C' && answer=== 'C', 'medium': answer === null && stuAnswer === 'C' }" @click="changeStuAnswer('C')">
			<div v-if="mode==='normal'">{{choice3}}</div>
			<input v-else style="width: calc(100% - 80px); padding: 4px 12px; background-color: #ffffff11; z-index: 0;" v-model="choice3"/>
			<!--用户选择错误答案-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'C' && answer !== 'C'" name="close-circle-filled" size="22px"></wd-icon>
			<!--正确-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'C' && answer === 'C'" name="check-circle-filled" size="22px"></wd-icon>
			<!--选择（无答案）-->
			<wd-icon color="#fff" v-if="answer === null && stuAnswer === 'C'" name="info-circle-filled" size="22px"></wd-icon>
		</div>
		<div class="xuanze-line dark-purple-card" :class="{'wrong': answer !== null && stuAnswer === 'D' && answer!== 'D', 'right': answer !== null && stuAnswer === 'D' && answer=== 'D', 'medium': answer === null && stuAnswer === 'D' }" @click="changeStuAnswer('D')">
			<div v-if="mode==='normal'">{{choice4}}</div>
			<input v-else style="width: calc(100% - 80px); padding: 4px 12px; background-color: #ffffff11; z-index: 0;" v-model="choice4"/>
			<!--用户选择错误答案-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'D' && answer !== 'D'" name="close-circle-filled" size="22px"></wd-icon>
			<!--正确-->
			<wd-icon color="#fff" v-if="answer !== null && stuAnswer === 'D' && answer === 'D'" name="check-circle-filled" size="22px"></wd-icon>
			<!--选择（无答案）-->
			<wd-icon color="#fff" v-if="answer === null && stuAnswer === 'D'" name="info-circle-filled" size="22px"></wd-icon>
		</div>
		<!--答案-->
		<div class="xuanze-line dark-purple-card choice-line" v-if="mode==='insert'">
			<div>标准答案：</div>
			<div :class="{'medium': answer === 'A'}" style="padding-left: 0;" class="choice-btn" @click="changeAnswer('A')">A</div>
			<div :class="{'medium': answer === 'B'}" class="choice-btn" @click="changeAnswer('B')">B</div>
			<div :class="{'medium': answer === 'C'}" class="choice-btn" @click="changeAnswer('C')">C</div>
			<div :class="{'medium': answer === 'D'}" style="margin-right: 20px;" class="choice-btn" @click="changeAnswer('D')">D</div>
		</div>
		
	</div>
</template>

<script setup>
	import { defineEmits, ref, defineProps, toRefs } from 'vue'
	
	const props = defineProps({
		choice1: String,
		choice2 :String,
		choice3: String,
		choice4: String,
		stuAnswer: String,
		answer: String,
		mode: String //默认normal为使用，insert为编辑OCR
	})
	const {choice1, choice2, choice3, choice4, stuAnswer, answer, mode} =toRefs(props)
	
	const emit = defineEmits(['changeStuAnswer', 'changeAnswer'])
	
	const changeStuAnswer = (newAnswer)=>{
		emit('changeStuAnswer', newAnswer)
	}
	const changeAnswer = (newAnswer)=>{
		emit('changeAnswer', newAnswer)
	}
	
</script>

<style>
	@import "@/css/global.css";
	@import "@/css/animation.css";
	.h1{
		animation: appear-ani .8s 1;
		font-weight: bold;
		letter-spacing: 1px;
		font-size: 17px;
		margin-bottom: 12px;
	}
	.xuanze-card{
		color: #222;
		padding: 12px 4px;
		white-space: pre-line;
		word-break: break-all;
		display: flex;
		flex-direction: column;
	}
	.xuanze-line{
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		padding: 8px 12px;
		margin: 4px 0;
		align-items: center;
		border-radius: 8px;
		border: 1px solid #4d80f088;
		transition: .4s;
		animation: bottom-in-ani .6s 1;
	}
	.xuanze-line view:nth-child(2){
		padding-left: 16px;
	}
	.right{
		background-color: #1ee80fcc;
		transition: .4s;
	}
	.wrong{
		background-color: #f71418cc;
		transition: .4s;
	}
	.medium{
		background-color: #4d80f0cc;
		transition: .4s;
	}
	.choice-btn{
		width: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		height: 20px;
		border-radius: 4px;
	}
</style>