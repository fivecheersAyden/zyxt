<template>
    <view class="choice-question">
        <CardCom title="题目">
            <view class="question">{{ exercise.problem }}</view>
        </CardCom>

        <CardCom title="选项">
            <radio-group @change="handleAnswerChange">
                
                <label v-for="(choice, index) in choices" :key="index" class="choice">
                    <radio :value="String.fromCharCode(65 + index)" :color="index == wrongOptionIndex? '#FF4040' : '#23a7f2' "/>
                    {{ choice }}
                </label>
            </radio-group>
        </CardCom>

        <button @click="submitExercise" v-if="!autoGetDetail?.auto" class="color-submit-button">提交</button>

        <!-- 提交后显示结果Card -->
        <view v-if="submitted" style="margin-top: 20px;" class="line-padding">
            <CardCom title="结果">
                <!-- 如果有传回的redoAnswer -->
                <view v-if="this.requestReceive.redoAnswer" class="line-padding">
                    <view class="tag">你的答案</view>
                    {{ this.requestReceive.redoAnswer }}
                </view>
                <!-- 如果有正确答案 -->
                <view v-if="exercise.answer" class="line-padding">
                    <view class="tag">正确答案</view>
                    {{ exercise.answer }}
                </view>
                <view class="line-padding">
                    <view v-if="this.requestReceive.redoAnswer === exercise.answer" class="tag-green">回答正确</view>
                    <view v-else class="tag-red">回答错误</view>
                </view>


                <view class="line-padding">
                    <view class="tag">解析</view>
                    {{ this.requestReceive.redoAIComment }}
                </view>
            </CardCom>
        </view>
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
            wrongOptionIndex: null,
            submitted: false,
            requestReceive: null,
            showLoading: false
        }
    },
    computed: {
        choices() {
            return [
                this.exercise.choice1,
                this.exercise.choice2,
                this.exercise.choice3,
                this.exercise.choice4
            ].filter(choice => choice !== null)
        }
    },
    methods: {
        handleAnswerChange(e) {
            console.log('单选题选项更改：', e.detail.value);
            this.exercise.stuAnswer = e.detail.value;
        },
        // 提交用户答案，获取AI分析结果
        submitExercise() {
            uni.showLoading({
                title: '加载中'
            });
            uni.request({
                url: globalProps.baseApi + '/redoRecord/v1',
                method: 'POST',
                header: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + globalProps.token
                },
                data: this.exercise,
                success: (res) => {
                    uni.hideLoading();
                    console.log(res.data);
                    // 在这里处理提交成功后的逻辑
                    this.requestReceive = res.data;
                    this.submitted = true;

                    // 判断正确错误
                    if (this.requestReceive.redoAnswer !== this.exercise.answer) {
                        this.wrongOptionIndex = this.exercise.answer.charCodeAt(0) - 66;
                        console.log('错误选项索引：', this.wrongOptionIndex)
                    }

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
        console.log('ChoiceQuestion onLoad')
        console.log(this.autoGetDetail)
        if (this.autoGetDetail?.auto) {
            // 如果是查看巩固历史，则自动获取详情
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
                    this.requestReceive = res.data;
                    this.submitted = true;
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
.choice-question {
    padding: 20px;
}

.question {
    font-weight: bold;
    margin-bottom: 10px;
}

.choice {
    display: block;
    margin-bottom: 5px;
    margin-left: 5px;
    margin-right: 5px;
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
    padding-top: 5px;
    padding-bottom: 5px;
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
