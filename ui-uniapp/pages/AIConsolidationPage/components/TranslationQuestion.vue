<template>
  <view class="translation-question">
    <CardCom title="题目">
      <view class="instructions">请将下面的句子翻译成英文:</view>
      <view class="content">{{ exercise.content }}</view>
    </CardCom>

    <CardCom title="作答" v-if="autoGetDetail?.auto">
      {{ redoAnswer }}
    </CardCom>

    <CardCom title="我的答案" v-else>
      <textarea class="answer-input" v-model="exercise.stuAnswer" placeholder="请输入你的翻译" />
    </CardCom>

    <button @click="submitExercise" v-if="!autoGetDetail?.auto" class="color-submit-button">提交</button>

    <view v-if="translateDetail" class="translate-detail">
      <CardCom title="结果">
        <view>
          <view class="tag">总分</view>
          {{ translateDetail.accuracyScore + translateDetail.fluencyScore + translateDetail.syntaxScore }}
        </view>
        <view>
          <view class="tag">详细建议</view>
          {{ translateDetail.detailedSuggestions }}
        </view>
        <view style="height: 20rpx;">
          <!-- placeholder -->
        </view>
        <view>
          <view class="tag">准确性评分</view>
          {{ translateDetail.accuracyScore }}
        </view>
        <view>
          <view class="tag">准确性评语</view>
          {{ translateDetail.accuracyComment }}
        </view>
        <view style="height: 20rpx;">
          <!-- placeholder -->
        </view>
        <view>
          <view class="tag">流畅性评分</view>
          {{ translateDetail.fluencyScore }}
        </view>
        <view>
          <view class="tag">流畅性评语</view>
          {{ translateDetail.fluencyComment }}
        </view>
        <view style="height: 20rpx;">
          <!-- placeholder -->
        </view>
        <view>
          <view class="tag">语法评分</view>
          {{ translateDetail.syntaxScore }}
        </view>
        <view>
          <view class="tag">语法评语</view>
          {{ translateDetail.syntaxComment }}
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
      translateDetail: null,
      redoAnswer: ''
    };
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
          this.translateDetail = res.data.translateDetail;
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
    console.log('TranslationQuestion onLoad')
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
          this.translateDetail = res.data.translateDetail;
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
.translation-question {
  padding: 20px;
}

.instructions {
  font-weight: bold;
  margin-bottom: 10px;
}

.content {
  margin-bottom: 10px;
}

.answer-input {
  width: 100%;
  height: 150px;
  /* padding: 15px; */
  /* border: 1px solid #ccc; */
  /* border-radius: 15px; */
  box-sizing: border-box;
}

.translate-detail {
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

.color-submit-button {
  background: linear-gradient(45deg, rgba(104, 0, 159, 1) 0%, rgba(63, 60, 132, 1) 100%);
  color: white;
  border-radius: 20px;
}
</style>
