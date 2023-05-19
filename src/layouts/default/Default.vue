<template>
  <v-app theme="dark">
    <mu-yu @addClick="addClick" @addCount="addCount" @updateText="b" :count="count" :click="click" :upd_time="time"/>
    <default-view />
    <base-layout-menu :islogin="isLogin" :offlinemode="offlineMode" :logindata="login"></base-layout-menu>
  </v-app>
</template>

<script setup>
  import DefaultView from './View.vue'
  import MuYu from './MuYu.vue';
  import BaseLayoutMenu from './BaseLayoutMenu.vue'
  import { ref } from 'vue';
  import Axios from 'axios';
  import { ElNotification } from 'element-plus';
  const count = ref('Loading...')
  const click = ref(0)
  var date = new Date()
  const time = ref("同步中")
  const isLogin = ref(false)
  const offlineMode = ref(false)
  let login = ref({})
  Axios.get('/api/user/info')
  .then(function(Response){
    time.value = date.toLocaleTimeString()
    if (Response['data']['code'] == 0){
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
    time.value = date.toLocaleTimeString()
    ElNotification.error({
      title: '注意',
      message: '无法访问后端服务，当前应用将以离线模式运行。您的未登录会话不受影响，但排行榜、注册登录等功能将无法使用。建议刷新页面'
    })
    offlineMode.value = true
  })

  const addCount = () => {
    count.value+=1
  }

  const addClick = () => {
    click.value+=1
  }

  const syncUserData = () => {
    Axios({
      url: '/api/user/sync',
      method: 'POST',
      data: {
        count: count.value,
        click_count: click.value
      }
    })
    .then(function(Response){
      var f = new Date()
      time.value = f.toLocaleTimeString() + " (同步成功)"
      if (Response['data']['code'] == 0){
        count.value = Response['data']['newValue']
        click.value = 0
        console.log(`同步成功，当前功德值为 ${Response['data']['newValue']} (北京时间 ${f.toLocaleTimeString()} 更新) `)
      }
      else{
        console.log('未登录，同步禁用')
      }
    })
  }

  setInterval(function(){
    syncUserData()
  }, 30000)

</script>
