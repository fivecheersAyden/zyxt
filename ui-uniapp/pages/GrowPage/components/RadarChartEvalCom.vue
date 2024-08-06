<template>
  <view class="question-type-card theme-card">
    <view class="title">能力维度</view>
    <view class="charts-box">
      <!-- 方便调试可设置canvas2d="false" -->
      <qiun-data-charts 
        type="radar"
        :opts="opts"
        :chartData="chartData"
        :inScrollView=true
        :canvas2d="true"
        canvasId="UcIpaUHhpGReBhpEhgGCSVcibpsyabcd"
        @getIndex="getIndex"
      />
    </view>
      <view v-if="currentIndex !== -1" class="detail">
        <view class="tag">评价</view>
        <!-- {{ this.abilityDimension.abilityDimensionDetail[currentIndex] }} -->
        {{ this.receivedData.abilityDimensionDetail[currentIndex] }}
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
            max: 10,
            labelShow: true,
            linearType: "custom",
            border: false
          }
        }
      }
    };
  },
  created() {
    // this.getServerData();
  },
  methods: {
    showData(obj){
      this.receivedData = obj;
      console.log('雷达Eval图子组件收到：', obj);
      let res = {
            categories: ["语言理解", "语言表达", "语言知识"],
            series: [
              {
                name: "能力维度",
                // data: [7, 8, 6] 
                data: obj.abilityDimensionData 
              }
            ]
          };
      this.chartData = JSON.parse(JSON.stringify(res));
    },
    // getServerData() {
    //   //模拟从服务器获取数据时的延时
    //   setTimeout(() => {
    //     //模拟服务器返回数据，如果数据格式和标准格式不同，需自行按下面的格式拼接
    //     let res = {
    //         categories: ["语言理解", "语言表达", "语言知识"],
    //         series: [
    //           {
    //             name: "能力维度",
    //             // data: [7, 8, 6] 
    //             data: this.abilityDimension.abilityDimensionData 
    //           }
    //         ]
    //       };
    //     this.chartData = JSON.parse(JSON.stringify(res));
    //   }, 500);
    // },
    getIndex(e){
			console.log(e.currentIndex)
      this.currentIndex = e.currentIndex
		},
  },
  // props: ['abilityDimension']
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
    background-color: rgb(47, 121, 195);
    color: white;
    padding: 2px 8px;
  }
  .detail{
    line-height: 1.5;
    margin-top: 15px;
  }

  .slide-fade-enter-active {
    transition: all 0.3s ease;
  }
  .slide-fade-leave-active {
    transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
  }
  .slide-fade-enter, .slide-fade-leave-to {
    transform: translateY(-10px);
    opacity: 0;
  }
</style>