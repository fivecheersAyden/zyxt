<template>
    <view class="reading-question">
        <CardCom title="文章">
            <view class="content">{{ content.replace(/\\'/g, "'") }}</view>
        </CardCom>

        <CardCom title="作答">
            <!-- 遍历所有小题题目question -->
            <view class="reading-question-container" v-for="(question, index) in receivedExercise.cuoTiList"
                :key="index">
                <view class="question-number">{{ index + 1 }}. {{ question.problem }}</view>
                <view class="options">
                    <radio-group @change="handleAnswerChange(question, $event)">
                        <!-- 如果有choice1 -->
                        <view v-if="question.choice1">
                            <radio class="option" :value="'A'" :key="'A'" :color="submitted && (question.answer !== redoRecords[index].redoAnswer)? '#FF4040' : '#23a7f2' ">{{ question.choice1 }}</radio>
                        </view>

                        <!-- 如果有choice2 -->
                        <view v-if="question.choice2">
                            <radio class="option" :value="'B'" :key="'B'" :color="submitted && (question.answer !== redoRecords[index].redoAnswer)? '#FF4040' : '#23a7f2' ">{{ question.choice2 }}</radio>
                        </view>

                        <!-- 如果有choice3 -->
                        <view v-if="question.choice3">
                            <radio class="option" :value="'C'" :key="'C'" :color="submitted && (question.answer !== redoRecords[index].redoAnswer)? '#FF4040' : '#23a7f2' ">{{ question.choice3 }}</radio>
                        </view>

                        <!-- 如果有choice4 -->
                        <view v-if="question.choice4">
                            <radio class="option" :value="'D'" :key="'D'" :color="submitted && (question.answer !== redoRecords[index].redoAnswer)? '#FF4040' : '#23a7f2' ">{{ question.choice4 }}</radio>
                        </view>

                    </radio-group>
                </view>
                <view class="analysis">
                    <view v-if="submitted">
                        <!-- <view>你的答案：{{ redoRecords[index].redoAnswer }}</view>
                        <view>正确答案：{{ question.answer }}</view> -->
                        <view v-if="redoRecords" class="line-padding">
                            <view class="tag">你的答案</view>
                            {{ redoRecords[index].redoAnswer }}
                        </view>
                        <view v-if="question.answer" class="line-padding">
                            <view class="tag">正确答案</view>
                            {{ question.answer }}
                        </view>
                        <view v-if="redoRecords[index].redoAnswer === question.answer" class="line-padding">
                            <view class="tag-green">回答正确</view>
                        </view>
                        <view v-else class="line-padding">
                            <view class="tag-red">回答错误</view>
                        </view>
                        <view class="line-padding">
                            <view class="tag">解析</view>
                            {{ redoRecords[index].redoAIComment }}
                        </view>
                    </view>
                </view>
                <view style="height: 30rpx;">
                    <!-- placeholder -->
                </view>
            </view>
        </CardCom>


        <button @click="submitExercise" v-if="!autoGetDetail?.auto" class="color-submit-button">提交</button>
    </view>
</template>

<script>
import { globalProps } from '@/js/global.js'
import CardCom from '@/components/CardCom.vue'

export default {
    components: {
        CardCom
    },
    props: {
        exercise: {
            type: Object,
            required: true
        },
        autoGetDetail: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            content: this.exercise.content,
            receivedExercise: this.exercise,
            submitted: false,
            readingAnalyzedInfo: null, // 分析返回的数据
        };
    },
    computed: {
        redoRecords() {
            return this.readingAnalyzedInfo?.redoRecords;
        }
    },
    watch: {
        redoRecords: function (newVal, oldVal) {
            console.log('redoRecords changed:', newVal, oldVal)
        }
    },
    methods: {
        handleAnswerChange(question, e) {
            console.log('阅读题选项更改：', e.detail.value);
            console.log('当前题目：', question)
            question.stuAnswer = e.detail.value
            console.log('更改后的当前题目：', question)
            // this.$emit('answer-changed', question)
        },
        // 提交当前receivedExercise以获取readingAnalyzedInfo /redoRecord
        submitExercise() {
            uni.showLoading({
                title: '加载中'
            });
            console.log("发送的数据：", this.receivedExercise)
            uni.request({
                url: globalProps.baseApi + '/redoRecord/v1',
                method: 'POST',
                header: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + globalProps.token
                },
                data: this.receivedExercise,
                success: (res) => {
                    uni.hideLoading();
                    console.log('分析返回：', res.data);
                    this.readingAnalyzedInfo = res.data;
                    this.submitted = true;
                    // 在这里处理提交成功后的逻辑
                },
                fail: (err) => {
                    uni.hideLoading();
                    console.error(err);
                    // 在这里处理提交失败后的逻辑
                }
            });
        }
    },
    mounted() {
        console.log('ReadingQuestion onLoad')
        console.log(this.autoGetDetail)
        if (this.autoGetDetail?.auto) {
            uni.request({
                url: globalProps.baseApi + '/redoRecord/detail/v1',
                method: 'GET',
                header: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + globalProps.token
                },
                data: {
                    recordID: this.autoGetDetail.redoId,
                    stuID: globalProps.userInfo.id
                },

                success: (res) => {
                    console.log(res.data);
                    // 在这里处理提交成功后的逻辑
                    this.submitted = true;
                    this.readingAnalyzedInfo = res.data;
                    this.receivedExercise = res.data;
                },
                fail: (err) => {
                    console.error(err);
                    // 在这里处理提交失败后的逻辑
                }
            });
        } else {
            console.log('没有自动获取详情')

        }
    }
}
</script>

<style>
.reading-question {
    padding: 20px;
}

.content {
    margin-bottom: 20px;
}

.reading-question-container {
    margin-bottom: 10px;
}

.question-number {
    font-weight: bold;
    margin-bottom: 5px;
}

.option {
    display: block;
    margin-bottom: 5px;
    margin-left: 10px;
    margin-right: 10px;
}

.redo-request {
    margin-top: 20px;
}

.analysis {
    margin-top: 10px;
}

.tag {
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: rgb(77, 74, 223);
    padding: 2px 8px;
}

.tag-green {
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: #52c41a;
    padding: 2px 8px;
}

.tag-red {
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: #ff4d4f;
    padding: 2px 8px;
}

.line-padding {
    padding: 5px 0;
}

.analysis {
    line-height: 1.5;
}

.color-submit-button {
    background: linear-gradient(45deg, rgba(104, 0, 159, 1) 0%, rgba(63, 60, 132, 1) 100%);
    color: white;
    border-radius: 20px;
}
</style>