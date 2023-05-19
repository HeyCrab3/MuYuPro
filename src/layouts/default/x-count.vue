<template>
    <div class="apollo-count">
        <h3 class="text-subtitle-1">{{ title }}</h3>
        <h1 class="text-h4">{{ count }}<span class="text-subtitle-1 click_times">(+{{ click_times }})</span></h1>
        <v-tooltip text="每三十秒更新一次数据"><template v-slot:activator="{ props }"><span class="text-subtitle-1" v-bind="props">北京时间 {{ upd_time }} 更新</span></template></v-tooltip>
    </div>
</template>

<style>
.apollo-count{
    margin-left: 20px;
    margin-top: 20px;
}
.click_times{
    margin-left: 20px;
    color: #ffe449
}
</style>

<script setup>
defineProps(['title', 'count', 'click_times', 'upd_time'])
</script>