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
				我的
			</view>
			<view style="width: 18px">
				<!-- placeholder for symmetry -->
			</view>
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<!--用户卡片-->
			<div class="usr-container">
				<!--logo-->
				<div class="logo-container">
					<image mode="aspectFit" src="../../static/logo.png"></image>
				</div>
				<!--用户名-->
				<div class="nickname-container">{{nickname}}</div>
			</div>
			<!--按钮-->
			<div class="btns-container">
				<!--使用说明-->
				<div @click="pageJump(0)" class="option-line">
					<wd-icon color="#222" name="help-circle" size="18px"></wd-icon>
					<div style="width: 8px;"></div>
					<div>使用说明</div>
					<div style="flex: 1;"></div>
					<wd-icon color="#222" name="arrow-right" size="22px"></wd-icon>
				</div>
				<!--在线客服-->
				<div @click="pageJump(1)" class="option-line">
					<wd-icon color="#222" name="call" size="18px"></wd-icon>
					<div style="width: 8px;"></div>
					<div>联系客服</div>
					<div style="flex: 1;"></div>
					<wd-icon color="#222" name="arrow-right" size="22px"></wd-icon>
				</div>
				<!--问题反馈-->
				<div @click="pageJump(2)" class="option-line">
					<wd-icon color="#222" name="edit-1" size="18px"></wd-icon>
					<div style="width: 8px;"></div>
					<div>问题反馈</div>
					<div style="flex: 1;"></div>
					<wd-icon color="#222" name="arrow-right" size="22px"></wd-icon>
				</div>
				<!--用户协议-->
				<div @click="pageJump(3)" class="option-line">
					<wd-icon color="#222" name="file" size="18px"></wd-icon>
					<div style="width: 8px;"></div>
					<div>用户协议</div>
					<div style="flex: 1;"></div>
					<wd-icon color="#222" name="arrow-right" size="22px"></wd-icon>
				</div>
				<!--占位-->
				<div style="flex: 1;"></div>
				<!--退出登录-->
				<div class="out-btn" @click="logOut">退出登录</div>
			</div>
		</view>
	</view>
</template>

<script setup>
	import { globalProps } from '@/js/global.js'
	import { onMounted, ref } from 'vue';
	
	onMounted(()=>{
		getNickName()
	})

	//获取userName
	const nickname = ref()
	const getNickName = ()=>{
		uni.getStorage({
			key: 'loginStorage',
			success(res) {
				nickname.value = res.data.userInfo.nickname
			}
		})
	}

	const logOut = ()=>{
		uni.removeStorageSync('loginStorage'); 
		uni.redirectTo({
			url:'/pages/LoginPage/LoginPage'
		})
	}
	const pageJump = (index)=>{
		let jumpUrl = ''
		switch(index){
			case 0:
				uni.showModal({
				  title: '使用说明',
				  content: globalProps.mineDocument,
				  showCancel: false, // 隐藏取消按钮，确保用户只能点击确认按钮关闭消息框
				  confirmText: '知道了'
				});
				break;
			case 1: 
				uni.setClipboardData({
				        data: globalProps.helperPhone,
				        success() {
				          uni.showToast({
				            title: '已复制客服电话',
				            icon: 'success'
				          });
				        }
				});
				break;
			case 2: 
				uni.setClipboardData({
				        data: globalProps.helperPhone,
				        success() {
				          uni.showToast({
				            title: '已复制客服电话',
				            icon: 'success'
				          });
				        }
				});
				break;
			case 3: 
				uni.showModal({
				  title: '使用说明',
				  content: globalProps.mineAgreement,
				  showCancel: false, // 隐藏取消按钮，确保用户只能点击确认按钮关闭消息框
				  confirmText: '知道了'
				});
				break;
		}
	}
</script>

<style>
@import url("@/css/global.css");
@import url("@/css/animation.css");
.tabbarpage-body{
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: space-between;
}
/*用户*/
.usr-container{
	height: 180px;
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: space-around;
	animation: top-in-ani .6s 1;
}
.logo-container{
	width: 90px;
	height: 90px;
	background-color: #fff;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 999px;
	border: 1px solid #4d80f0;
	margin-left: 12px;
}
.logo-container image{
	width: 72px;
}
.nickname-container {
	width: 200px;
	font-size: 21px;
	
}
/*按钮*/
.btns-container{
	border-top: 1px solid #4d80f022;
	width: calc(100% - 24px);
	flex: 1;
	background-color: #f6f9ff;
	animation: bottom-in-ani .6s 1;
	border-top-left-radius: 12px;
	border-top-right-radius: 12px;
	padding: 20px 12px 12px 12px;
	display: flex;
	flex-direction: column;
}
.option-line{
	display: flex;
	align-items: center;
	justify-content: space-between;
	height: 40px;
	letter-spacing: 2px;
	border: #ddd 1px solid;
	border-radius: 8px;
	padding: 6px 12px;
	margin: 4px 0;
	background: linear-gradient(to right, #ffffff22, #b3c6f911);
}
.out-btn{
	display: flex;
	align-items: center;
	justify-content: center;
	height: 32px;
	letter-spacing: 2px;
	border: #ddd 1px solid;
	border-radius: 8px;
	padding: 6px 12px;
	margin: 6px 0;
	background-color: #4d80f0;
	color: #fff;
	box-shadow: 2px 2px 4px #00000011;
}

</style>
