<template>
    <view class="container">
        <input class="input" v-model="text" placeholder="请输入要合成的文本" />
        <button class="btn" @click="synthesizeText">合成语音</button>
    </view>
</template>

<script>
import crypto from 'crypto-js'

export default {
    data() {
        return {
            text: '',
            innerAudioContext: null
        }
    },
    methods: {
        synthesizeText() {
            if (!this.text) {
                uni.showToast({
                    title: '请输入要合成的文本',
                    icon: 'none'
                })
                return
            }

            const appKey = '7475d4fa19dec914'
            const appSecret = '4tTqxrz1a9RxPn3jFKhjqtLAvhgshcqG'
            const salt = this.generateUUID()
            const curtime = Math.floor(new Date().getTime() / 1000)
            const input = this.getInput(this.text)
            const sign = this.generateSign(appKey, input, salt, curtime, appSecret)

            const requestData = {
                q: this.text,
                appKey,
                salt,
                sign,
                signType: 'v3',
                curtime,
                format: 'mp3',
                voiceName: 'youxiaoqin'
            }

            uni.request({
                url: 'https://openapi.youdao.com/ttsapi',
                method: 'POST',
                data: this.buildFormData(requestData),
                responseType: 'arraybuffer',
                success: (res) => {
                    console.log(res.data)
                    const audioData = res.data
                    this.playAudio(audioData)
                },
                fail: (err) => {
                    console.error(err)
                    uni.showToast({
                        title: '语音合成失败',
                        icon: 'none'
                    })
                }
            })
        },
        playAudio(audioData) {
            this.innerAudioContext = uni.createInnerAudioContext()
            this.innerAudioContext.autoPlay = true
            this.innerAudioContext.src = audioData
            this.innerAudioContext.onError((err) => {
                console.error('播放音频发生错误:', err)
            })
        },
        getInput(text) {
            const textLength = text.length
            if (textLength > 20) {
                return `${text.substr(0, 10)}${textLength}${text.substr(-10)}`
            } else {
                return text
            }
        },
        generateUUID() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                const r = (Math.random() * 16) | 0
                const v = c === 'x' ? r : (r & 0x3) | 0x8
                return v.toString(16)
            })
        },
        generateSign(appKey, input, salt, curtime, appSecret) {
            const str = `${appKey}${input}${salt}${curtime}${appSecret}`
            return crypto.SHA256(str).toString()
        },
        buildFormData(data) {
            const formData = new FormData()
            for (const key in data) {
                formData.append(key, data[key])
            }
            return formData
        }
    }
}
</script>

<style>
.container {
    padding: 20px;
}

.input {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
}

.btn {
    background-color: #007aff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>