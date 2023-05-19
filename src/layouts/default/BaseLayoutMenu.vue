<template>
    <div class="bottom-navbar">
        <v-menu location="top" style="margin-bottom: 20px;">
            <template v-slot:activator="{ props }">
                <v-btn icon="mdi-menu" v-bind="props"></v-btn>
                <div class="text">
                    <h2 style="display: inline-block; font-weight: 500; font-size: 1.4rem; margin-left: 20px;">电子木鱼</h2>
                    <h3 style="display: inline-block; font-weight: 500; font-size: 0.9rem; margin-left: 20px;">v0.2</h3>
                </div>
            </template>
            <v-list style="margin-bottom: 20px;" class="rounded-xl">
                <v-list-item @click="click(0,1)" v-if="offlinemode == false && islogin == false" :key="1" variant="plain" title="登录/注册" subtitle="登录以同步多端数据"><template v-slot:prepend><v-icon icon="mdi-account"/></template></v-list-item>
                <v-list-item v-if="islogin == true && offlinemode == false" :key="1" variant="plain" :title="logindata['nick']" :subtitle="`${logindata['phone']} | 点击查看用户信息`"><template v-slot:prepend><v-avatar :image="logindata['avatar']"/></template></v-list-item>
                <v-list-item v-if="offlinemode == true" :key="1" variant="plain" title="离线模式" disabled subtitle="请检查网络连接并刷新页面"><template v-slot:prepend><v-icon icon="mdi-network-off-outline"/></template></v-list-item>
                <v-list-item @click="click(index, item.nav)" :key="index" variant="plain" v-for="(item, index) in menuItem" :title="item.title" :subtitle="item.text">
                    <template v-slot:prepend>
                        <v-icon :icon="item.icon"></v-icon>
                    </template>
                </v-list-item>
            </v-list>
        </v-menu>
    </div>
    <v-dialog persistent v-model="isShow">
        <v-card>
            <v-card-text>
                <h2 class="text-h5" style="margin-bottom: 20px;">欢迎登录</h2>
                <v-alert type="error" :style="{'margin-bottom': '10px', 'display': err == null ? 'none' : 'block'}" :text="err"/>
                <v-form>
                    <v-text-field required :loading="isLoading" v-model="phoneNumber" label="手机号">
                        <template v-slot:prepend>
                            <v-icon icon="mdi-phone"></v-icon>
                        </template>
                    </v-text-field>
                    <v-text-field required :loading="isLoading" v-model="code" label="短信验证码">
                        <template v-slot:prepend>
                            <v-icon icon="mdi-message"></v-icon>
                        </template>
                        <template v-slot:append>
                            <v-btn variant="tonal" color="primary" :disabled="isInTimeout" :loading="isLoading" @click="sendCode">{{ btnText }}</v-btn>
                        </template>
                    </v-text-field>
                    <v-card-actions style="margin-left: 15px; margin-bottom: 20px;">
                        <v-btn :loading="isLoading" variant="tonal" size="large" color="primary" @click="loginWithSMS">登录</v-btn>
                        <v-btn :disabled="isLoading" variant="tonal" size="large" @click="isShow = false">以游客身份继续</v-btn>
                    </v-card-actions>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
    <first-login :is-show="b" :phone-number="c"/>
</template>

<style scoped>
    .bottom-navbar{
        float: left;
        margin-left: 30px;
        margin-bottom: 30px;
    }
    .text{
        position: relative;
        top: 4px;
        display: inline-block;
    }
</style>

<script lang="ts" setup>
defineProps(['offlinemode', 'logindata', 'islogin'])

import { ref } from 'vue';
import { ElMessage } from 'element-plus'
import Axios from 'axios'
import FirstLogin from './FirstLogin.vue'

let captcha_data = ref({})
let isInTimeout = ref(false)
let btnText = ref('发送验证码')
let isLoading = ref(false)
let captcha_public = ref(null)
const err = ref(null)
const isShow = ref(false)
const phoneNumber = ref(null)
const code = ref(null)
const b = ref(false)
const c = ref(0)

const menuItem = ref([
    {
        title: '排行榜',
        text: '查看今天是谁把佛祖刷到了榜二',
        icon: 'mdi-format-list-bulleted',
        nav: '2'
    },
    {
        title: 'GitHub',
        text: '给个star',
        icon: 'mdi-github',
        nav: '3'
    },
    {
        title: '关于应用',
        text: 'v0.2.1',
        icon: 'mdi-information-outline',
        nav: '4'
    }
])

const loginWithSMS = () => {
    err.value = null
    if (phoneNumber.value == null || code.value == null){
        err.value = '请填写手机号和验证码'
    }
    else{
        isLoading.value = true
        Axios({
            url: '/api/user/login',
            method: 'POST',
            data: {
                phone: phoneNumber.value,
                sms_code: code.value
            }
        })
        .then(function(Response){
            isLoading.value = false
            if (Response['data']['code'] == 0){
                ElMessage.success('登陆成功')
                isShow.value = false;
            }
            else if(Response['data']['code'] == 1){
                console.log('账号未初始化，等待用户操作')
                isShow.value = false;
                b.value = true;
                c.value = phoneNumber.value
            }else{
                err.value = Response['data']['msg']
            }
        })
        .catch(function(error){
            err.value = error
        })
    }
}

function getSMSCode(phoneNumber){
    err.value = null
    Axios({
        url: '/api/sms/send',
        method: 'POST',
        data: {
            phone: phoneNumber
        }
    })
    .then(function(Response){
        isLoading.value = false
        if (Response['data']['code'] == 0){
            let countdown = 120
            isInTimeout.value = true
            var a = setInterval(function(){
                countdown-=1
                btnText.value = `${countdown} s后重发`
                if (countdown <= 0){
                    clearInterval(a)
                    isInTimeout.value = false
                    btnText.value = `点击重发验证码`
                }
            }, 1000)
        }else{
            err.value = Response['data']['msg']
            captcha_public.value.reset()
        }
    })
}

initGeetest4({
    captchaId: '21a42f0d13be9e79670e136fd786dfc8',
    product: 'bind'
}, function(captcha){
    captcha_public.value = captcha
    captcha.onSuccess(function(){
        captcha_data.value = captcha.getValidate()
        isLoading.value = true
        Axios({
            url: '/api/captcha/verify',
            method: 'POST',
            data: {
                lot_number: captcha_data.value.lot_number,
                captcha_output: captcha_data.value.captcha_output,
                pass_token: captcha_data.value.pass_token,
                gen_time: captcha_data.value.gen_time,
            }
        })
        .then(function(Response){
            isLoading.value = false
            if (Response['data']['code'] == 0){
                getSMSCode(phoneNumber.value)
            }else{
                ElMessage.error(Response['data']['msg'])
                captcha_public.value.reset()
            }
        })
        .catch(function(error){
            isLoading.value = false
            err.value = '发生错误，请重试'
        })
    })
    captcha.onError(function(error){err.value = `发生错误：${error.msg} (${error.code})`})
})

const click = (key, navigation) => {
    if (navigation == '1'){
        isShow.value = true
    }
}

const sendCode = () => {
    err.value = null
    if (phoneNumber.value == null){
        err.value = "请填写手机号"
    }
    else{
        captcha_public.value.showCaptcha()
    }
}
</script>