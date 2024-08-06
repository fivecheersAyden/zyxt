<template>
    <view class="essay-question">
        <CardCom title="题目">
            <view class="instructions">{{ exercise.content }}</view>
        </CardCom>

        <CardCom title="作答" v-if="autoGetDetail?.auto">
            {{ redoAnswer }}
        </CardCom>
        <CardCom title="作答" v-else>
            <textarea class="answer-input" v-model="exercise.stuAnswer" placeholder="请在此处写作" />
        </CardCom>

        <button @click="submitExercise" v-if="!autoGetDetail?.auto" class="color-submit-button">提交</button>
        <view v-if="essayDetail" class="essay-detail">
            <CardCom title="评价">
                <view>
                    <view class="tag">总分</view>
                    {{ essayDetail.contentScore + essayDetail.structureScore + essayDetail.syntaxScore }}
                </view>
                <view>
                    <view class="tag">详细建议</view>
                    {{ essayDetail.detailedSuggestions }}
                </view>
                <view style="height: 20rpx;">
                    <!-- placeholder -->
                </view>
                <view>
                    <view class="tag">内容评分</view>
                    {{ essayDetail.contentScore }}
                </view>
                <view>
                    <view class="tag">内容评语</view>
                    {{ essayDetail.contentComment }}
                </view>
                <view style="height: 20rpx;">
                    <!-- placeholder -->
                </view>
                <view>
                    <view class="tag">组织结构评分</view>
                    {{ essayDetail.structureScore }}
                </view>
                <view>
                    <view class="tag">组织结构评语</view>
                    {{ essayDetail.structureComment }}
                </view>
                <view style="height: 20rpx;">
                    <!-- placeholder -->
                </view>
                <view>
                    <view class="tag">语法评分</view>
                    {{ essayDetail.syntaxScore }}
                </view>
                <view>
                    <view class="tag">语法评语</view>
                    {{ essayDetail.syntaxComment }}
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
            essayDetail: null,
            redoAnswer: ''
        }
    },
    methods: {
        submitExercise() {
            uni.showLoading({
                title: '加载中'
            });
            uni.request({
                url: globalProps.baseApi + '/redoRecord/v1', // 修改为你的提交接口
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
                    this.essayDetail = res.data.compositionDetail;
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
        console.log('EssayQuestion onLoad')
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
                    this.essayDetail = res.data.compositionDetail;
                    this.redoAnswer = res.data.redoAnswer;
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
.essay-question {
    padding: 20px;
}

.instructions {
    margin-bottom: 10px;
}

.answer-input {
    width: 100%;
    height: 300px;
    /* padding: 10px; */
    /* border: 1px solid #ccc; */
    /* border-radius: 4px; */
    box-sizing: border-box;
}

.essay-detail {
    margin-top: 20px;
}

.tag {
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: rgb(77, 74, 223);
    padding: 2px 8px;
    margin-top: 20rpx;
}

.tag-green {
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: #52c41a;
    padding: 2px 8px;
    margin-top: 20rpx;
}

.tag-red {
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: #ff4d4f;
    padding: 2px 8px;
    margin-top: 20rpx;
}

.color-submit-button{
    background: linear-gradient(45deg, rgba(104, 0, 159, 1) 0%, rgba(63, 60, 132, 1) 100%);
    color: white;
    border-radius: 20px;
}
</style>