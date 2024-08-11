# ling-imgcropper
# |属性	|类型	|默认	|备注|
|:-:		|:-:	|:-:	|:-:													|
|url		|String	|""		|需要裁剪的图片路径，为空时控件隐藏，不为空时控件显示	|
|fixed		|Boolean|false	|是否固定大小											|
|width		|Number	|200	|图片裁剪后的宽度，固定大小时有效						|
|height		|Number	|200	|图片裁剪后的高度，固定大小时有效						|
|maxWidth	|Number	|1024	|图片裁剪后的最大宽度，非固定大小时有效					|
|maxHeight	|Number	|1024	|图片裁剪后的最大高度，非固定大小时有效					|
|blob		|Boolean|true	|是否将base64转化为blob，H5模式下有效					|
事件名称	  说明	               返回
ok	     点击确定按钮	      e:{path}
cancel	 点击取消按钮	

新版本新增参数说明:
参数iszoom,为false的话按设备像素比来裁剪与传入的crop-width和crop-height相同比例的图片，
为true的话则为固定为传入的crop-width和crop-height的尺寸。补充一下，传入的参数都要在image-cropper和canvas 里各写一份。
新增了裁剪尺寸像素比个性化设置参数，只要传入proportion参数不为0的参数就可以设置裁剪的图片放大多少倍，注意放大的越高性能就越差，如果不是非不得已请不要设置，默认为零。

示例：
<template>
    <view>
        <button @tap="upload">上传</button>
        <image-cropper :src="tempFilePath" @confirm="confirm" @cancel="cancel"></image-cropper>
        <image :src="cropFilePath" mode="aspectFit" style="width: 100%;"></image>
			<!--  #ifdef MP-ALIPAY -->
<canvas  id="myCanvas" canvas-id="myCanvas"   class="meslist_canvas" crop-width="200" crop-height="200"></canvas>

	 <!--  #endif-->  
    </view>
	
</template>
export default {
    data() {
        return {
            tempFilePath: '',
            cropFilePath: '',
        }
    },
    components: {ImageCropper},
    methods: {
        upload() {
            uni.chooseImage({
                count: 1, //默认9
                sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
                sourceType: ['album'], //从相册选择
                success: (res) => {
                    this.tempFilePath = res.tempFilePaths.shift()
                }
            });
        },
        confirm(e) {
            this.tempFilePath = ''
            this.cropFilePath = e.detail.tempFilePath
        },
        cancel() {
            console.log('canceled')
        }
    },
}
<style>
.meslist_canvas{position: fixed;top:0;width: 200px;height: 200px;visibility: hidden;}
</style>