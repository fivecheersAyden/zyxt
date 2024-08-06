<template>
	<view class="tabbarpage-container">
		<view class="status_bar">
			<!-- 这里是状态栏 -->
		</view>
		<view class="page-header-back">
			<navigator open-type="navigateBack" hover-class="navigator-hover">
				<view class="back-icon">
					<wd-icon name="thin-arrow-left" size="18px"></wd-icon>
				</view>
			</navigator>
			<view class="title">
				图片裁剪
			</view>
			<view style="width: 18px"></view>
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<!--裁剪组件-->
			<div class="cut-container">
				 <bt-cropper autoZoom="false" ref="cropper" :imageSrc="photo"></bt-cropper>
			</div>
			<!--确定按钮-->
			<div class="btn-container">
				<div class="scale-container">
					<wd-icon name="refresh" size="22px"></wd-icon>
				</div>
				<wd-button @click="ocrBtn">确定</wd-button>
				<div>
					<wd-icon name="refresh" size="22px"></wd-icon>
				</div>
			</div>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				photo:''
			}
		},
		onLoad(options) {
			this.photo = decodeURIComponent(options.photo);
		},
		methods: {
			ocrBtn(){
				//获取文件
				this.$refs.cropper.crop().then((res)=>{
					uni.saveFile({
					  tempFilePath: res,
					  success(res) {
						uni.$emit('getPhotoCut', res.savedFilePath)
					    console.log('文件保存成功', savedFilePath);
					  },
					  fail(err) {
					    console.error('文件保存失败', err);
					  }
					});
					uni.navigateBack()
				})
			},
		},
	}
</script>

<style>
@import url("@/css/global.css");
@import url("@/css/animation.css");
.all-container{
	position: fixed;
	left: 0;
	right: 0;
	top: 20px;
	bottom: 0;
}
.cut-container{
	position: absolute;
	top: 0;
	right: 0;
	left: 0;
	bottom: 52px;
	background-color: #aaa;
}
.btn-container{
	position: absolute;
	bottom: 0;
	height: 52px;
	display: flex;
	align-items: center;
	justify-content: space-around;
	left: 0;
	right: 0;
	padding: 0 12vw;
	background-color: #e6e7ee;
}
.scale-container{
	transform: scaleX(-1);
}
</style>
