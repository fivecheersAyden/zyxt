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
				第{{ currentIndex + 1 }}题  {{ quesTypeTranslated }}
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>

		</view>
        
        <view class="tabbarpage-body scrollable" style="padding-bottom: 60rpx;">
            <!-- <view class="question-container">
                <view class="question-index">第{{ currentIndex + 1 }}题  {{ currentExercise.category }}</view>
            </view> -->
            <view v-if="currentExercise.category === 'xuanze'">
                <!-- <choice-question :exercise="currentExercise" @answer-changed="handleAnswerChanged"></choice-question> -->
                <choice-question :exercise="currentExercise"></choice-question>
            </view>
            <view v-else-if="currentExercise.category === 'yuedu'">
                <!-- <reading-question :exercise="currentExercise" @answer-changed="handleAnswerChanged"></reading-question> -->
                <reading-question :exercise="currentExercise"></reading-question>
            </view>
            <view v-else-if="currentExercise.category === 'fanyi'">
                <translation-question :exercise="currentExercise"
                    ></translation-question>
                    <!-- @answer-changed="handleAnswerChanged"></translation-question> -->
            </view>
            <view v-else-if="currentExercise.category === 'zuowen'">
                <!-- <essay-question :exercise="currentExercise" @answer-changed="handleEssayAnswerChanged" /> -->
                <essay-question :exercise="currentExercise" />
            </view>
            <view v-else>题型错误</view>
            <view class="button-container">
                <button @click="previousQuestion" :disabled="currentIndex === 0" class="color-button">上一题</button>
                <button @click="nextQuestion" :disabled="currentIndex === exerciseList.length - 1" class="color-button">下一题</button>
            </view>
        </view>
    </view>

</template>

<script>
import { globalProps } from '@/js/global.js'
import ChoiceQuestion from './components/ChoiceQuestion.vue'
import ReadingQuestion from './components/ReadingQuestion.vue'
import TranslationQuestion from './components/TranslationQuestion.vue'
import EssayQuestion from './components/EssayQuestion.vue'
import quesTypeTranslator from '@/js/quesTypeTranslator.js'

export default {
    components: {
        ChoiceQuestion,
        ReadingQuestion,
        TranslationQuestion,
        EssayQuestion,
    },
    data() {
        return {

            // 数据
            exerciseList: [], // 从外部接收exerciseList数据
            currentIndex: 0
        }
    },
    onLoad() {
        // 获取传递的参数
        this.exerciseList = uni.getStorageSync('exerciseList');
        console.log("QuestionShowPage中：", this.exerciseList)
    },
    computed: {
        currentExercise() {
            console.log('currentIndex:', this.currentIndex)
            console.log('this.exerciseList[', this.currentIndex, '] = ', this.exerciseList[this.currentIndex])
            return this.exerciseList[this.currentIndex]
        },
        quesTypeTranslated() {
            return quesTypeTranslator(this.currentExercise.category)
        }
    },
    methods: {
        // handleAnswerChanged(answer) {
        //     // 处理用户答案变化的逻辑
        //     this.currentExercise.stuAnswer = answer
        // },
        // handleEssayAnswerChanged(answer) {
        //     // 处理用户提交的作文答案
        //     console.log('用户提交的作文答案:', answer)
        // },
        previousQuestion() {
            if (this.currentIndex > 0) {
                this.currentIndex--
            }
            setTimeout(() => {
                uni.pageScrollTo({
                    scrollTop: 0, // 将滚动位置设置为顶部
                    duration: 0 // 滚动到顶部的动画时长，单位为毫秒
                });
            })
        },
        nextQuestion() {
            if (this.currentIndex < this.exerciseList.length - 1) {
                this.currentIndex++
            }
            setTimeout(() => {
                uni.pageScrollTo({
                    scrollTop: 0, // 将滚动位置设置为顶部
                    duration: 0 // 滚动到顶部的动画时长，单位为毫秒
                });
            })
        }
    }
}
</script>

<style>
@import "@/css/global.css";
@import "@/css/animation.css";


.button-container {
    display: flex;
    justify-content: space-around;
    /* margin-top: 20px; */
}

.question-container {
    padding: 10px;
    font-size: large;
}

.question-index{
    font-size: 20px;
    font-weight: bold;
    /* 居中 */
    text-align: center;
}

.color-button{
    background: linear-gradient(to right bottom, #1c3364, #19035b);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 5px;
    width: 40%;
    /* font-size: 16px; */
    text-align: center;
}


</style>