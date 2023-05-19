<template>
    <div class="apollo-count">
        <h3 class="text-subtitle-1">{{ title }}</h3>
        <h1 class="text-h4">{{ count }}</h1>
    </div>
</template>

<style>
.apollo-count{
    margin-left: 20px;
    margin-top: 20px;
}
</style>

<script setup>
defineProps(['title', 'count'])
</script>