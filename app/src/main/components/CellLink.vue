<template>
    <router-link :to="to" :class="linkClass">
        {{ text }}
    </router-link>
</template>

<script setup>
const props = defineProps({
    to: String,
    text: String,
    linkClass: {
        type: String,
        default: 'text-neutral-900 hover:text-neutral-700'
    }
})
</script>