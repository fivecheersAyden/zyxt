<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
			// 禁止横屏
			// #ifdef APP-PLUS
			plus.screen.lockOrientation("portrait-primary")
			// #endif
			
		},
		onShow: function() {
			
		},
		onHide: function() {
			
		}
	}
</script>

<style>
	/*每个页面公共css */
</style>
