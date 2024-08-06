<template>
    <view class="card-template theme-card">
        <view class="card-header">
            {{ title }}
        </view>
		<view class="card-content">
            <slot></slot>
		</view>
    </view>
</template>

<script setup>
import { defineProps } from 'vue';
defineProps({
    title: String
})

</script>

<script>
export default {
  options: {
    virtualHost: true
  }
}
</script>

<style>
    body{
        margin-top: 20px;
    }
    .card-template{
        display: flex;
        flex-direction: column;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .card-template:last-child{
        margin-bottom: 0;
    }
    .card-header{
        font-size: large;
        font-weight: bold;
        margin-bottom: 20px;
    }
</style>