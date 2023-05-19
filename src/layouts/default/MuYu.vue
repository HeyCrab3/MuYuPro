<template>
    <x-count title="功德值" :count="count" :click_times="click" :upd_time="upd_time"></x-count>
    <svg @click="clicked" :class="className" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" style="height: 350px; width: 350px;"><path d="M542.8 554.6c-21.8 0-41.1-10.9-52.6-27.6-12.6 3.7-25.9 5.7-39.6 5.7H254.1c-14.6 0-28.8-2.3-42.1-6.5-11.5 17.1-31 28.3-53.1 28.3-35.3 0-64-28.7-64-64 0 88 72 160 160 160h192c88 0 160-72 160-160-0.1 35.5-28.7 64.1-64.1 64.1zM904.2 627.5l-198-174.6c-3.3-2.9-8.2-2.8-11.1 0.1l-6.3 6.3c-2.9 2.9-3 7.9-0.1 11.1l174.6 198c17 19.3 38.6 30.3 46.5 22.4l16.9-16.9c7.8-7.8-3.2-29.4-22.5-46.4z" fill="#FFFFFF"></path><path d="M698.5 424.3l1.8-1.8c28.5-28.5-25.7-67.7-61.7-75l-23.3-4.7c-8.6-1.7-17.7 1.4-22.8 6.5l-7.5 7.5c-5.1 5.1-8.3 14.2-6.5 22.8l4.7 23.3c0.5 2.5 1.2 5.2 2 7.9-27.8-47.8-79.5-80-138.4-80h-192c-88 0-160 72-160 160 0-35.3 28.7-64 64-64s64 28.7 64 64c0 1.8-0.1 3.7-0.2 5.5 10.1 3.1 20.7 4.7 31.5 4.7h196.6c9.8 0 19.3-1.3 28.5-3.8-0.2-2.1-0.3-4.2-0.3-6.3 0-35.3 28.7-64 64-64s64 28.7 64 64c0-18.1-3.1-35.5-8.7-51.8 15.9 25.8 40.5 45.3 60.1 25.7l1.8-1.8c-2.3-10.3 0.5-21.5 8.4-29.4l0.6-0.6c7.9-8.3 19.2-11.1 29.4-8.7z" fill="#FFFFFF"></path></svg>
</template>

<style>
.icon{
    margin: auto;
    margin-top: 10%
}

.v-clicked {
    animation: clicked 0.2s ease-in-out
}

@keyframes clicked {
    0%{
        transform: scale(1);
    }
    50%{
        transform: scale(1.1);
    }
    100%{
        transform: scale(1);
    }
}

</style>

<script lang="ts" setup>
import { ref } from 'vue';
import xCount from './x-count.vue';

defineProps(['count', 'upd_time', 'click'])
let className = ref("icon")

const emit = defineEmits<{
    (event: "addCount"): void;
    (event: "addClick"): void;
}>();

const clicked = () => {
    className.value = "icon v-clicked"
    setTimeout(function(){className.value = "icon"}, 300)
    emit("addCount")
    emit("addClick")
}

</script>