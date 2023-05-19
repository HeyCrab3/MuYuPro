<template>
    <v-dialog persistent :model-value="isShow">
        <v-card>
            <v-card-text>
                <h2 class="text-h5" style="margin-bottom: 20px;">欢迎回来</h2>
                <h2 class="text-subtitle-1" style="margin-bottom: 20px;">完善一下基本信息，然后出发吧！</h2>
                <v-alert type="error" :style="{'margin-bottom': '10px', 'display': err == null ? 'none' : 'block'}" :text="err"/>
                <v-form>
                    <v-text-field :disabled="true" :model-value="phoneNumber" label="手机号">
                        <template v-slot:prepend>
                            <v-icon icon="mdi-phone"></v-icon>
                        </template>
                    </v-text-field>
                    <v-text-field :clearable="true" :loading="isLoading" v-model="nick" required label="你的昵称">
                        <template v-slot:prepend>
                            <v-icon icon="mdi-account"></v-icon>
                        </template>
                    </v-text-field>
                    <v-text-field :clearable="true" :loading="isLoading" v-model="avatar" required label="头像">
                        <template v-slot:prepend>
                            <v-icon icon="mdi-account"></v-icon>
                        </template>
                        <template v-slot:append>
                            <v-btn href="https://img.1r2.cc" target="_blank" variant="tonal" color="primary" :disabled="isLoading">打开图床</v-btn>
                        </template>
                    </v-text-field>
                    <v-card-actions style="margin-left: 15px; margin-bottom: 20px;">
                        <v-btn :loading="isLoading" variant="tonal" size="large" color="primary" @click="register">让我们开始吧</v-btn>
                    </v-card-actions>
                </v-form>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup>
defineProps(['isShow', 'phoneNumber'])
import { ref } from 'vue'
import { ElMessage } from 'element-plus';
import Axios from 'axios';
const isLoading = ref(false)
const nick = ref(null)
const err = ref(null)
const avatar = ref('https://dimples-1337.heycrab.xyz/uploads/QQ%E5%9B%BE%E7%89%8720230514154134.jpg')

const register = () => {
    err.value = null;
    if (nick.value == null || avatar.value == null){
        err.value = "请填写所有的数据"
    }
    else{
        isLoading.value = true
        Axios({
            url: '/api/user/register',
            method: 'POST',
            data: {
                nick: nick.value,
                avatar: avatar.value
            }
        })
        .then(function(Response){
            isLoading.value = false
            if (Response['data']['code'] == 0){
                ElMessage.success('注册完成，页面将在五秒后刷新')
                setTimeout(function(){window.location.reload()}, 5000)
            }else{
                err.value = Response['data']['msg']
            }
        })
        .catch(function(error){
            isLoading.value = false
            err.value = error
        })
    }
}
</script>