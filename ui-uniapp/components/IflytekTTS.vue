<template>
	<view>
		<input v-model="tip" placeholder="请输入要合成的文字">
		<button @click="readText">测试</button>
		<button @click="playMp3">测试播放mp3</button>
	</view>
</template>

<script setup>
import {
	ref
} from 'vue'
import CryptoJS from 'crypto-js'
import {
	fromByteArray
} from 'base64-js'
import {
	Buffer
} from 'buffer'

const tip = ref("我测试你的吗")

const config = {
	hostUrl: 'wss://tts-api.xfyun.cn/v2/tts',
	host: 'tts-api.xfyun.cn',
	appid: '34f37d0c',
	apiSecret: 'NjdlYjMwODQ4ZDgyY2RiNzlkMTA3MjZl',
	apiKey: 'cbe8d9d3d0e6bf32bcfbee5a15e7616e',
	uri: '/v2/tts'
}
function getAuthStr(date) {
	let signatureOrigin = `host: ${config.host}\ndate: ${date}\nGET ${config.uri} HTTP/1.1`
	let signatureSha = CryptoJS.HmacSHA256(signatureOrigin, config.apiSecret)
	let signature = CryptoJS.enc.Base64.stringify(signatureSha)
	let authorizationOrigin = `api_key="${config.apiKey}", algorithm="hmac-sha256", headers="host date request-line", signature="${signature}"`
	let authStr = CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(authorizationOrigin))
	return authStr
}

const playMp3 = () => {
	let innerAudioContext = uni.createInnerAudioContext();
	innerAudioContext.src = 'https://www.yym-free.com/resource/default/mp3/ed24da8f-cce3-4f61-9a83-1d929d0403aa.mp3';
	innerAudioContext.play()
}

const readText = () => {
	if (tip.value == "") {
		return
	}
	let date = (new Date().toUTCString())
	let wssUrl = config.hostUrl + "?authorization=" + getAuthStr(date) + "&date=" + date + "&host=" + config.host
	// 创建 WebSocket 连接
	let socketTask = uni.connectSocket({
		url: wssUrl,
		success: (res) => {
			console.log(res)
		},
		fail: (err) => {
			console.log(err)
		}
	})

	console.log(socketTask)
	//连接建立完毕，读取数据识别
	let buff = []
	let nowAudio = 0;
	let innerAudioContext = uni.createInnerAudioContext();

	socketTask.onOpen(() => {
		console.log("websocket connect!")
		// send(text) //传输数据
		let frame = {
			"common": {
				"app_id": config.appid
			},
			// 填充business
			"business": {
				"aue": "lame",
				"auf": "audio/L16;rate=16000",
				"vcn": "xiaoyan",
				"tte": "UTF8",
				"sfl": 1
			},
			// 填充data
			"data": {
				"text": Buffer.from(tip.value).toString('base64'),
				"status": 2
			}
		}
		socketTask.send({
			data: JSON.stringify(frame)
		})

		socketTask.onMessage((res) => {
			let res_data = JSON.parse(res.data)
			console.log(res_data)

			// 解码音频数据
			let audioData = res_data.data.audio;
			buff.push(audioData)
			if (res_data.code == 0 && res_data.data.status == 2) {
				//状态为2才表示合成结束，需要合并           
				socketTask.close()
				playAudio(0); //开始播放音频
			}
		})
	})

	function playAudio(cur) {
		if (cur >= buff.length) {
			innerAudioContext.stop()
			return;
		}
		innerAudioContext.src = 'data:audio/mp3;base64,' + buff[cur];
		innerAudioContext.onCanplay(() => {
			innerAudioContext.play()
			innerAudioContext.onEnded(() => {
				playAudio(cur + 1); //递归调用下一次播放
			})
		})
		// // 调用该函数，传入接收到的音频数据 buff
		// playAudioFromBuffer(buff);
	}


	// 试图使用uni.getFileSystemManager保存mp3
	// const fs = uni.getFileSystemManager();

	// function playAudioFromBuffer(buffer) {
	// 	const filePath = `${uni.env.USER_DATA_PATH}/audio.mp3`;
	// 	const uint8Array = new Uint8Array(buffer); // 将数组转换为 Uint8Array
	// 	con
	// 	fs.writeFile({
	// 		filePath: filePath,
	// 		data: uint8Array.buffer, // 使用 buffer 属性作为数据
	// 		encoding: 'base64',
	// 		success: () => {
	// 			// console.log('写入文件成功', filePath);
	// 			// innerAudioContext.src = filePath;
	// 			// innerAudioContext.play();
	// 			// innerAudioContext.onEnded(() => {
	// 			// 	console.log('音频播放结束');
	// 			// });

	// 			uni.playVoice({
	// 				filePath: filePath,
	// 				complete: () => {
	// 					// 播放完成后的回调
	// 					// 可以在这里删除本地的音频文件
	// 					fs.unlink({
	// 						filePath: filePath,
	// 						success: () => {
	// 							console.log('音频文件删除成功');
	// 						},
	// 						fail: (err) => {
	// 							console.log('音频文件删除失败', err);
	// 						}
	// 					});
	// 				}
	// 			});
	// 		},
	// 		fail: (err) => {
	// 			console.log('写入文件失败', err);
	// 		}
	// 	});
	// }

	
	// 试图保存mp3
	// function playAudioFromBuffer(buffer) {
	// 	const filePath = plus.io.convertLocalFileSystemURL("_downloads/") + 'audio.mp3'; // 存储路径，示例为根目录下的audio.mp3

	// 	plus.io.requestFileSystem(plus.io.PUBLIC_DOWNLOADS, (fs) => {
	// 		fs.root.getFile(filePath, {
	// 			create: true
	// 		}, (fileEntry) => {
	// 			fileEntry.createWriter((writer) => {
	// 				writer.onwrite = () => {
	// 					const localUrl = plus.io.convertLocalFileSystemURL(filePath);
	// 					uni.playVoice({
	// 						filePath: localUrl,
	// 						complete: () => {
	// 							// 播放完成后的回调
	// 							// 可以在这里删除本地的音频文件
	// 							fileEntry.remove(() => {
	// 								console.log('音频文件删除成功');
	// 							}, (err) => {
	// 								console.log('音频文件删除失败', err);
	// 							});
	// 						}
	// 					});
	// 				};
	// 				writer.write(new Blob([buffer], {
	// 					type: 'audio/mp3'
	// 				}));
	// 			}, (err) => {
	// 				console.log('创建文件写入器失败', err);
	// 			});
	// 		}, (err) => {
	// 			console.log('获取文件失败', err);
	// 		});
	// 	}, (err) => {
	// 		console.log('请求文件系统失败', err);
	// 	});
	// }
}

</script>

<style></style>