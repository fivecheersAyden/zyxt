<template>
  <view class="question-type-card theme-card">
    <view class="title">我的能力曲线</view>
    <view class="charts-box">
      <!-- 方便调试可设置canvas2d="false" -->
      <qiun-data-charts 
        type="line"
        :opts="opts"
        :chartData="chartData"
        :inScrollView=true
        :canvas2d="true"
        canvasId="NTUkjbYqfZqLJlUooyjdMhwxDlVZSIJf"
        @getIndex="getIndex"
      />
    </view>
    <view v-if="currentIndex !== -1">
      <view class="detail">
        
        <view v-if="this.receivedData.suggestions[currentIndex] !== null && this.receivedData.suggestions[currentIndex] !== ''">
          <view class="tag">建议</view>
          {{ this.receivedData.suggestions[currentIndex] }}
        </view>
        <view v-else>
          <view class="tag">建议</view>
          哎呀，老师没看到你在这周有错题记录呢，继续加油哦！
        </view>
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
      //您可以通过修改 config-ucharts.js 文件中下标为 ['line'] 的节点来配置全局默认参数，如都是默认参数，此处可以不传 opts 。实际应用过程中 opts 只需传入与全局默认参数中不一致的【某一个属性】即可实现同类型的图表显示不同的样式，达到页面简洁的需求。
      opts: {
        color: ["#1890FF","#91CB74","#FAC858","#EE6666","#73C0DE","#3CA272","#FC8452","#9A60B4","#ea7ccc"],
        padding: [15,10,0,15],
        dataLabel: false,
        dataPointShape: false,
        enableScroll: false,
        legend: {
          show: false
        },
        xAxis: {
          disableGrid: true,
		  fontColor: "#FFFFFF"
        },
        yAxis: {
          gridType: "dash",
          dashLength: 2,
		  fontColor: "#FFFFFF",
          data: [
            {
              min: 0,
              max: 10
            }
          ]
        },
        extra: {
          line: {
            type: "curve",
            width: 2,
            activeType: "hollow",
            linearType: "custom",
            onShadow: true,
            animation: "horizontal"
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
      console.log('line图子组件收到：', obj);
      let res = {
            categories: ["5周前","4周前","3周前","2周前","1周前","本周"],
            series: [
              {
                name: "用户能力",
                linearColor: [
                  [
                    0,
                    "#1890FF"
                  ],
                  [
                    0.25,
                    "#00B5FF"
                  ],
                  [
                    0.5,
                    "#00D1ED"
                  ],
                  [
                    0.75,
                    "#00E6BB"
                  ],
                  [
                    1,
                    "#90F489"
                  ]
                ],
                setShadow: [
                  3,
                  8,
                  10,
                  "#1890FF"
                ],
                // data: [35,8,25,37,4,20] 
                data: obj.lineData
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
    //         categories: ["5周前","4周前","3周前","2周前","1周前","本周"],
    //         series: [
    //           {
    //             name: "用户能力",
    //             linearColor: [
    //               [
    //                 0,
    //                 "#1890FF"
    //               ],
    //               [
    //                 0.25,
    //                 "#00B5FF"
    //               ],
    //               [
    //                 0.5,
    //                 "#00D1ED"
    //               ],
    //               [
    //                 0.75,
    //                 "#00E6BB"
    //               ],
    //               [
    //                 1,
    //                 "#90F489"
    //               ]
    //             ],
    //             setShadow: [
    //               3,
    //               8,
    //               10,
    //               "#1890FF"
    //             ],
    //             // data: [35,8,25,37,4,20] 
    //             data: this.overallPerformanceWithTime.lineData
    //           }
    //         ]
    //       };
    //     this.chartData = JSON.parse(JSON.stringify(res));
    //   }, 500);
    // },
    getIndex(e){
			console.log(e.currentIndex.index)
      this.currentIndex = e.currentIndex.index
		},
  },
  // props: ['overallPerformanceWithTime']
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
    margin-bottom: 20px;
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
</style>