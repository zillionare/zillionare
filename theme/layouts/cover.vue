<script setup lang="ts">
import { computed } from 'vue'
import { handleBackground } from '../layoutHelper'

const props = defineProps({
  background: {
    default: '/public/ribbon.jpg',
  }
})

const style = computed(() => handleBackground(props.background, false))

</script>
<style>
.title {
        position: absolute;
        top: 15%;
        width:100%;
        font-size: 4vw !important;
        color: white;
    }

.summary {
    position:absolute;
    top: 50%;
    left: 2rem;
    color: rgb(56, 11, 119);
    h1 {
        font-size: 7vw !important;
    }
}

.slogan {
    position: absolute;
    top: 6rem;
    left: 2rem;
    font-style: italic;
    font-family: gothic;
    color: rgb(56, 11, 119);
    font-size: xx-large;
}

.mask {
    background-color: rgba(88,88,88, 0.2);
    backdrop-filter: blur(10px);
    position: absolute;
    width:100%;
    top: 20%;
    height: 40%;
    left:0;
}

.seq {
    color: white;
    position:absolute;
    font-family: monospace;
    left: 2rem;
    top: 3rem;
    font-size: xx-large;
}
</style>
<template>
<div
class="slidev-layout cover text-center"
:style="style"
>
    <div class="mask">
    <h1 class="my-auto w-full title">
        {{ $slidev.nav.currentRoute.meta.title }}
        <hr style="position: absolute;top:22%">
    </h1>
    <div class="summary">
        <slot />
    </div>
</div>
<div class="slogan">
    {{ $slidev.nav.currentRoute.meta.slogan }}
</div>
<div class="seq">
    {{ $slidev.nav.currentRoute.meta.seq }}
</div>
</div>
</template>
