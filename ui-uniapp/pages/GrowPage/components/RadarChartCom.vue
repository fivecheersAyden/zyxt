<template>
  <view class="question-type-card theme-card">
    <view class="title">题型得分率</view>
    <view class="charts-box">
      <!-- 方便调试可设置canvas2d="false" -->
      <qiun-data-charts 
        type="radar"
        :opts="opts"
        :chartData="chartData"
        :canvas2d="true"
        :inScrollView=true
        canvasId="UcIpaUHhpGReBhpEhgGCSVcibpsyISTV"
        @getIndex="getIndex"
      />
    </view>
    <view v-if="currentIndex !== -1">
      <view class="detail">
        <view class="tag">表现</view>
        <!-- {{ this.questionTypeCorrectRate.correctRateDetail[currentIndex].performance }} -->
        {{ this.receivedData.correctRateDetail[currentIndex].performance }}
      </view>

      <view class="detail">
        <view class="tag">建议</view>
        <!-- {{ this.questionTypeCorrectRate.correctRateDetail[currentIndex].suggestions }} -->
        {{ this.receivedData.correctRateDetail[currentIndex].suggestions }}
      </view>
    </view>

  </view>
</template>

<script>
export default {
  data() {
    return {
      receivedData: {},
      currentIndex: -1,
      chartData: {},
      //您可以通过修改 config-ucharts.js 文件中下标为 ['radar'] 的节点来配置全局默认参数，如都是默认参数，此处可以不传 opts 。实际应用过程中 opts 只需传入与全局默认参数中不一致的【某一个属性】即可实现同类型的图表显示不同的样式，达到页面简洁的需求。
      opts: {
        color: ["#1890FF","#91CB74","#FAC858","#EE6666","#73C0DE","#3CA272","#FC8452","#9A60B4","#ea7ccc"],
        padding: [5,5,5,5],
        dataLabel: true,
        dataPointShape: false,
        enableScroll: false,
        legend: {
          show: false,
          position: "right",
          lineHeight: 25
        },
        extra: {
          radar: {
            gridType: "circle",
            gridColor: "#CCCCCC",
            gridCount: 3,
            opacity: 1,
            max: 1,
            labelShow: true,
            linearType: "custom",
            border: false,
			labelColor: "#FFFFFF"
          }
        }
      }
    };
  },
  created() {
    
    // console.log('题型雷达图子组件收到：', this.questionTypeCorrectRate)
    
  },
  methods: {
    showData(obj){
      this.receivedData = obj
      console.log('雷达图子组件收到：', obj);
      let res = {
            // categories: ["翻译题", "选择题", "阅读题", "作文题"],
            categories: ["选择题", "阅读题", "翻译题", "作文题"],
            series: [
              {
                name: "成绩分布",
                // data: [90, 70, 30, 88] // 假设这是学生在各题型上的得分百分比
                data: obj.correctRateData // 假设这是学生在各题型上的得分百分比
              }
            ]
          };
      this.chartData = JSON.parse(JSON.stringify(res));
    },
    getIndex(e){
			console.log(e.currentIndex)
      this.currentIndex = e.currentIndex
		},
  },
  // props: ['questionTypeCorrectRate']
};
</script>

<style scoped>
  /* 请根据实际需求修改父元素尺寸，组件自动识别宽高 */
  .charts-box {
    width: 100%;
    height: 200px;
  }
  .question-type-card{
    display: flex;
    flex-direction: column;
    padding: 15px;
    border-radius: 15px;
    
  }
  .title{
    font-size: large;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .tag{
    display: inline-block;
    width: fit-content;
    box-sizing: content-box;
    border-radius: 10px;
    background-color: rgb(77,74,223);
    padding: 2px 8px;
  }
  .detail{
    line-height: 1.5;
    margin-top: 15px;
  }
</style>