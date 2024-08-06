<script>
	// import { ref, defineExpose, onMounted, defineProps, watch } from 'vue';
	
	// /**
	//  * 配置
	//  */
	// //额度配置
	// const speech_rate = ref(0)
	// const myAppkey = ref('2hfVbAU7ahbvM4a2')
	// const myToken = ref('60eebdec27154673b05d31cf8200c977')
	// //角色
	// const { role } = defineProps({
	//     role: {
	// 		type: String,
	//         default: 'zhixiaoxia'
	//     }
	// })
	// /**
	//  * 消息
	//  */
	// //存储待播放的序列
	// const msgList = ref([])
	// //添加消息进入序列
	// const addMsg = (msg)=>{
	// 	msgList.value.push(msg)
	// 	playList()
	// }
	// /**
	//  * 播放
	//  */
	// //播放器
	// const innerAudioContext = ref(null)
	// //播放状态
	// const isPlaying = ref(false)
	// //播放列表
	// const playList = ()=>{
	// 	if (isPlaying.value || msgList.value.length === 0) {
	// 	    return;
	// 	}
	// 	isPlaying.value = true;
	// 	playTillEmpty();
	// }
	// //播放直到msgList为空
	// const playTillEmpty = ()=>{
	// 	let sentence = msgList.value.shift()
	// 	console.log(sentence)
	// 	if (!sentence) {
	// 		isPlaying.value = false;
	// 	    uni.$emit('endTalk')
	// 	    return;
	// 	}
	// 	let encodeText = encodeURIComponent(sentence)
	// 	innerAudioContext.value.src = 'https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts?appkey=' + myAppkey.value + '&speech_rate=' + speech_rate.value + '&voice=' + role + '&token=' + myToken.value + '&text=' + encodeText + `&format=wav&sample_rate=16000`;
	// 	innerAudioContext.value.play()
	// 	innerAudioContext.value.onEnded(() => {
	// 		playTillEmpty()
	// 	});
	// }
	// //强制清空播放器
	// const clearAudioContext = ()=>{
	// 	msgList.value = []
	// 	if (innerAudioContext.value.src || innerAudioContext.value.srcObject) {
	// 	        innerAudioContext.value.stop(); // 停止音频播放
	// 	    }
	// 	uni.$emit('endTalk')
	// }
	// /**
	//  * 全局方法
	//  */
	// onMounted(()=>{
	// 	innerAudioContext.value = uni.createInnerAudioContext()
	// })
	// defineExpose({addMsg, playTillEmpty, clearAudioContext})
	
export default {
		data() {
				return {
					voice: 'zhixiaoxia',
					innerAudioContext: null,
					tip: '样例文字',
					queue: [],
					isPlaying: false,
					speech_rate: 144, // 默认速度0，[-500, 0, 500] 对应的语速倍速区间为 [0.5, 1.0, 2.0]
					myAppkey: '2hfVbAU7ahbvM4a2',
					myToken: '',
				}
			},
        methods: {
			setVoice(newVoice){
				this.voice = newVoice
			},
			setSpeed(newSpeed){
				this.speech_rate = newSpeed
			},
            addMsgToQueue(msg) {
                this.queue.push(msg);
                this.playQueue();
            },
            playQueue() {
                if (this.isPlaying || this.queue.length === 0) {
                    return;
                }
				uni.$emit('startTalk')
				this.$emit('start-tts')
                this.isPlaying = true;
                this.playNext();
            },
            playNext() {
				let that = this
				uni.request({
					url: 'https://www.yym-free.com/wz/aliyuntoken',
					method: 'GET',
					success(res) {
						if(res.data === 'false'){
							uni.showToast({
								icon: 'error',
								title: '流式语音token过期'
							})
						}else{
							let sentence = that.queue.shift();
							if (!sentence) {
							    that.isPlaying = false;
							    uni.$emit('endTalk')
								that.$emit('end-tts')
							    return;
							}
							that.innerAudioContext = uni.createInnerAudioContext();
							let encodeText = encodeURIComponent(sentence)
							console.log('音频播放源','https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts?appkey=' + that.myAppkey + '&speech_rate=' + that.speech_rate + '&voice=' + that.voice + '&token=' + res.data + '&text=' + encodeText + `&format=wav&sample_rate=16000`)
							that.innerAudioContext.src = 'https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts?appkey=' + that.myAppkey + '&speech_rate=' + that.speech_rate + '&voice=' + that.voice + '&token=' + res.data + '&text=' + encodeText + `&format=wav&sample_rate=16000`;
							that.innerAudioContext.play();
							that.innerAudioContext.onEnded(() => {
							    that.playNext();
							});
						}
						
					}
				})
            },
			clearChat(){
				console.log('TTS终止')
				this.isPlaying = false;
				this.queue = []
				uni.$emit('endTalk')
				this.$emit('end-tts')
				if (this.innerAudioContext !== null) {
				    this.innerAudioContext.stop();
				}
			}
        },
        emits: ['start-tts', 'end-tts']
}
</script>
