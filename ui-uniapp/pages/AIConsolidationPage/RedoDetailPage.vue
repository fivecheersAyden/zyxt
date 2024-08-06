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
                巩固历史
            </view>
            <view style="width: 18px">
                <!-- placeholder for symmetry -->
            </view>

        </view>
        <view class="tabbarpage-body scrollable" style="padding-bottom: 60rpx;">
            <view v-if="currentExercise.category === 'xuanze'">
                <!-- <choice-question :exercise="currentExercise" @answer-changed="handleAnswerChanged"></choice-question> -->
                <choice-question :exercise="currentExercise" :auto-get-detail="autoGetDetail" />
            </view>
            <view v-else-if="currentExercise.category === 'yuedu'">
                <!-- <reading-question :exercise="currentExercise" @answer-changed="handleAnswerChanged"></reading-question> -->
                <reading-question :exercise="currentExercise" :auto-get-detail="autoGetDetail" />
            </view>
            <view v-else-if="currentExercise.category === 'fanyi'">
                <translation-question :exercise="currentExercise" :auto-get-detail="autoGetDetail" />
                    <!-- @answer-changed="handleAnswerChanged"></translation-question> -->
            </view>
            <view v-else-if="currentExercise.category === 'zuowen'">
                <!-- <essay-question :exercise="currentExercise" @answer-changed="handleEssayAnswerChanged" /> -->
                <essay-question :exercise="currentExercise" :auto-get-detail="autoGetDetail" />
            </view>
            <view v-else>题型错误</view>
            <!-- <view class="button-container">
                <button @click="previousQuestion" :disabled="currentIndex === 0">上一题</button>
                <button @click="nextQuestion" :disabled="currentIndex === exerciseList.length - 1">下一题</button>
            </view> -->
        </view>
    </view>

</template>

<script>
import { globalProps } from '@/js/global.js'
import ChoiceQuestion from './components/ChoiceQuestion.vue'
import ReadingQuestion from './components/ReadingQuestion.vue'
import TranslationQuestion from './components/TranslationQuestion.vue'
import EssayQuestion from './components/EssayQuestion.vue'

export default {
    components: {
        ChoiceQuestion,
        ReadingQuestion,
        TranslationQuestion,
        EssayQuestion
    },
    data() {
        return {
            // 全局属性
            statusBarHeight: globalProps.statusBarHeight,
            capsuleHeight: globalProps.capsuleHeight,

            // 数据
            // exerciseList: [], // 从外部接收exerciseList数据
            // currentIndex: 0

            autoGetDetail: {
                auto: true,
                redoId: '',
            }
        }
    },
    onLoad(option) {
        if(option){
            console.log("RedoDetailPage中：", option)
            this.currentExercise.category = option.category
            this.autoGetDetail.redoId = option.redoId
        }
    },
    computed: {
        currentExercise() {
            // console.log('currentIndex:', this.currentIndex)
            // console.log('this.exerciseList[', this.currentIndex, '] = ', this.exerciseList[this.currentIndex])
            // return this.exerciseList[this.currentIndex]
            return uni.getStorageSync('redoItem')
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
        // previousQuestion() {
        //     if (this.currentIndex > 0) {
        //         this.currentIndex--
        //     }
        //     setTimeout(() => {
        //         uni.pageScrollTo({
        //             scrollTop: 0, // 将滚动位置设置为顶部
        //             duration: 0 // 滚动到顶部的动画时长，单位为毫秒
        //         });
        //     })
        // },
        // nextQuestion() {
        //     if (this.currentIndex < this.exerciseList.length - 1) {
        //         this.currentIndex++
        //     }
        //     setTimeout(() => {
        //         uni.pageScrollTo({
        //             scrollTop: 0, // 将滚动位置设置为顶部
        //             duration: 0 // 滚动到顶部的动画时长，单位为毫秒
        //         });
        //     })
        // }
    }
}
</script>

<style>
@import "@/css/global.css";
@import "@/css/animation.css";

.button-container {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
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
</style>