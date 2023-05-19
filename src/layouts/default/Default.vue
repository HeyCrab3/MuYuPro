<template>
  <v-app theme="dark">
    <x-count title="功德值" :count="count"></x-count>
    <default-view />
    <base-layout-menu :islogin="isLogin" :offlinemode="offlineMode" :logindata="login"></base-layout-menu>
  </v-app>
</template>

<script setup>
  import DefaultView from './View.vue'
  import BaseLayoutMenu from './BaseLayoutMenu.vue'
  import xCount from './x-count.vue';
  import { ref } from 'vue';
  import Axios from 'axios';
  import { ElNotification } from 'element-plus';
  const count = ref('Loading...')
  const isLogin = ref(false)
  const offlineMode = ref(false)
  let login = ref({})
  Axios.get('/api/user/info')
  .then(function(Response){
    if (Response['data']['code'] == 0){
      console.log(Response['data'])
      count.value = Response['data']['data']['point']
      login.value = Response['data']['data']
      isLogin.value = true
    }
    else{
      ElNotification.warning({
        title: '建议登录',
        message: '我们建议您登陆，登录后数据多端漫游且可以使用排行榜功能'
      })
      count.value = 0
      isLogin.value = false
    }
  })
  .catch(function(){
    ElNotification.error({
      title: '注意',
      message: '无法访问后端服务，当前应用将以离线模式运行。您的未登录会话不受影响，但排行榜、注册登录等功能将无法使用。建议刷新页面'
    })
    offlineMode.value = true
  })
</script>
