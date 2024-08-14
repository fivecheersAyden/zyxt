<template>
	<view class="tabbarpage-container">
		<view class="status_bar">
		    <!-- 这里是状态栏 -->
		</view>
		<view class="page-header">
			
		</view>
		<!--主体-->
		<view class="tabbarpage-body">
			<!--LOGO-->
			<div class="logo-container">
				<image mode="aspectFit" src="@/static/logo.png" alt="" />
				<h1>智悦学途</h1>
				<h3>您的智能英语教辅</h3>
			</div>
			<!--表单-->
			<div class="form-container">
				<!--登陆表单-->
				<div class="form-body" v-if="!mode">
					<wd-form ref="form" :model="model">
					  <wd-cell-group border>
					    <wd-input
					      label="用户名"
					      label-width="100px"
					      clearable
					      v-model="model.login.nickname"
					      placeholder="请输入用户名"
					      :rules="[{ required: true, message: '请填写用户名' }]"
					    />
					    <wd-input
					      label="密码"
					      label-width="100px"
					      show-password
					      clearable
					      v-model="model.login.password"
					      placeholder="请输入密码"
					      :rules="[{ required: true, message: '请填写密码' }]"
					    />
					  </wd-cell-group>
					  <view class="footer">
					    <wd-button type="primary" size="large" @click="loginSure" block>登录</wd-button>
					  </view>
					</wd-form>
					<div class="card-bottom" @click="changeMode">没有账户？点击注册</div>
				</div>
				<!--注册表单-->
				<div class="form-body" v-else>
					<wd-form ref="form" :model="model">
					  <wd-cell-group border>
					    <wd-input
					      label="用户名"
					      label-width="100px"
					      clearable
					      v-model="model.signup.nickname"
					      placeholder="请输入用户名"
					      :rules="[{ required: true, message: '请填写用户名' }]"
					    />
					    <wd-input
					      label="密码"
					      label-width="100px"
					      show-password
					      clearable
					      v-model="model.signup.password"
					      placeholder="请输入密码"
					      :rules="[{ required: true, message: '请填写密码' }]"
					    />
						<wd-input
						  label="确认密码"
						  label-width="100px"
						  show-password
						  clearable
						  v-model="model.signup.checkpassword"
						  placeholder="确认密码"
						  :rules="[{ required: true, message: '请填写密码' }]"
						/>
					  </wd-cell-group>
					  <view class="footer">
					    <wd-button type="primary" size="large" @click="signUpSure" block>注册</wd-button>
					  </view>
					</wd-form>
					<div class="card-bottom" @click="changeMode">返回登录</div>
				</div>
				<!--其他登陆方式-->
				<wd-divider style="color:white; width: 100%; margin: 12px 0;">其他方式登录</wd-divider>
				<div class="other-container">
					<image @click="otherLogin(1)" mode="aspectFit" src="@/static/icon_QQ.png" alt="" />
					<image @click="otherLogin(2)" mode="aspectFit" src="@/static/icon_weichat.png" alt="" />
					<image @click="otherLogin(3)" mode="aspectFit" src="@/static/icon_zhifubao.png" alt="" />
				</div>
			</div>
			<!--使用问题-->
			<div class="problem-container">
				<p @click="showProblem">使用问题</p>
			</div>
		</view>
	</view>
</template>

<script setup>
	import { globalProps } from '@/js/global.js'
	import { onMounted, ref } from 'vue';
	
	const mode = ref(false)//0为登录 1为注册
	const model = ref({
		login:{
			nickname:null,
			password:null
		},
		signup:{
			nickname:null,
			password:null,
			checkpassword:null
		}
	})
	const changeMode = ()=>{
		mode.value = !mode.value
	}
	onMounted(()=>{
		loginJump()
	})
	const loginSure = ()=>{
		uni.request({
		  url: globalProps.baseApi + 'authenticate/login',
		  method: 'POST',
		  data: model.value.login,
		  success: function(res) {
		    console.log(res)
			if(res.statusCode === 200){
				//登陆成功
				var currentTime = new Date()
				var oneHourLater = new Date(currentTime.getTime() + globalProps.remeberAccountTime * 60000);
				const loginStorage = {
					endTime: oneHourLater,
					userInfo: res.data.user,
					token: res.data.token
				}
				uni.setStorage({
				  key: 'loginStorage',
				  data: loginStorage,
				});
				loginJump()
			}else{
				uni.showToast({
					icon:"error",
					title:res.data.message
				})
			}
		  },
		  fail: function(err) {
		    console.error(err)
			uni.showToast({
				icon:"error",
				title:"登陆失败，请重试"
			})
		  }
		})
	}
	const signUpSure = ()=>{
		if(model.value.signup.checkpassword !== model.value.signup.password){
			uni.showToast({
				icon:"error",
				title:"两次输入密码不同"
			})
			return
		}
	    uni.request({
	      url: globalProps.baseApi + 'authenticate/register',
	      method: 'POST',
	      data: model.value.signup,
	      success: function(res) {
	        console.log(res)
	    	if(res.statusCode === 200){
	    		model.value.login.nickname = model.value.signup.nickname
				model.value.login.password = model.value.signup.password
				loginSure()
	    	}else{
	    		uni.showToast({
	    			icon:"error",
	    			title:res.data.message
	    		})
	    	}
	      },
	      fail: function(err) {
	        console.error(err)
	    	uni.showToast({
	    		icon:"error",
	    		title:"注册失败，请重试"
	    	})
	      }
	    })
	}
	const loginJump = ()=>{
		uni.getStorage({
			key: 'loginStorage',
			success(loginStorage) {
				var currentTime = new Date()
				if(currentTime.getTime() > new Date(loginStorage.data.endTime).getTime()){
					//登陆过期
					uni.showToast({
						icon:"none",
						title:"登陆过期，请重新登录"
					})
					showWarn()
				}else{
					//自动登录
					console.log(loginStorage.data)
					globalProps.token = loginStorage.data.token
					globalProps.userInfo = loginStorage.data.userInfo
					console.log('自动登陆成功，token和userInfo如下')
					console.log(globalProps.token)
					console.log(globalProps.userInfo)
					uni.switchTab({
						url:"/pages/HomePage/HomePage"
					})
					uni.showToast({
						icon:"success",
						title:"自动登陆成功"
					})
				}
			},
			fail(e) {
				showWarn()
				console.log('首次登陆'+JSON.stringify(e))
			}
		})
	}
	const showWarn = ()=>{
		setTimeout(()=>{
					uni.showModal({
							  title: '提示',
							  content:
							   `
（1）本软件处于测试开发阶段，受限于api额度显示，部分功能可能不稳定，如遇到使用问题，请联系客服调整。
				
（2）软件测试账号：root，密码：root
			
（3）软件包含ocr智能识题功能，您可以自备题目或通过点击下方链接下载示例题目。`,
							  showCancel: true, // 隐藏取消按钮，确保用户只能点击确认按钮关闭消息框
							  confirmText: '跳转下载',
							  cancelText:'我知道了',
							  cancelColor: '#007aff',
							  success(res) {
							  	if(res.confirm){
									plus.runtime.openURL('https://www.yym-free.com/resource/default/zip/fb529fec-c942-48e4-9206-9b36d118aede.zip')
									/* uni.setClipboardData({
									        data: 'https://www.yym-free.com/resource/default/zip/fb529fec-c942-48e4-9206-9b36d118aede.zip',
									        success() {
									          uni.showToast({
									            title: '已复制下载地址',
									            icon: 'success'
									          });
									        }
									}); */
								}
							  }
							});
				},1000)
	}
	const showProblem = ()=>{
		uni.setClipboardData({
		  data: '13552461269',
		  success: function () {
		    uni.showToast({
		      icon:"none",
		      title:"客服联系方式已复制"
		    });
		  }
		});

		
	}
	const otherLogin = (type)=>{
		uni.showToast({
			icon: 'none',
			title: '暂不支持'
		})
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
/*logo*/
.logo-container{
	width: 90%;
	height: 220px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}
.logo-container image{
	height: 82px;
	animation: bottom-in-ani 1s 1;
}
.logo-container h1{
	color: #496cf1ff;
	letter-spacing: 6px;
	font-weight: bold;
	font-size: 40px;
	margin: -12px 0 4px 0;
	animation: text-ani 1s 1;
	white-space: nowrap;
}
.logo-container h3{
	font-size: 14px;
	color: #496cf1;
	letter-spacing: 2px;
	animation: text-ani 1s 1;
	white-space: nowrap;
}

/*表单*/
.form-container{
	width: 90%;
	flex: 0.96;
	display: flex;
	flex-direction: column;
	align-items: center;
	animation: bottom-in-ani 1s 1;
}
.form-body{
	padding: 20px 12px;
	background-color: #fff;
	border-radius: 8px;
	box-shadow: 2px 2px 8px #00000011;
}
.form-body button{
	margin-top: 20px;
}
.form-body .card-bottom{
	text-align: end;
	font-size: 12px;
	margin: 12px 4px -4px 0;
	color: #406bc8ff;
	text-decoration: underline;
}
.other-container{
	height: 40px;
	width: 100%;
	align-items: center;
	display: flex;
	justify-content: space-around;
	flex-direction: row;
	position: relative;
}
.other-container image{
	height: 100%;
}


/*问题*/
.problem-container{
	width: 90%;
	height: 20px;
	margin-bottom: 16px;
	display: flex;
	align-items: center;
	justify-content: center;
}
.problem-container p{
	font-size: 14px;
	text-decoration: underline;
	color: #666;
}
:deep(.uni-modal__bd){
	text-align: left !important;
}

</style>
