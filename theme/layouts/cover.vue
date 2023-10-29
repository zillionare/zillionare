<script setup lang="ts">
import { computed } from 'vue'
import { handleBackground } from '../layoutHelper'

const props = defineProps({
  background: {
    default: 'https://images.jieyu.ai/images/2023/10/portfolio-optimisation.png',
  }
})

const style = computed(() => {
    return {
        background: 'no-repeat url("/public/ribbon.jpg")',
        backgroundSize: 'cover',
        opacity: 0.85,
        zIndex:-1
    }
})

const maskStyle = computed(() => {
    return {
        background: `url(${props.background})`,
        backgroundSize: 'cover',
        opacity: 0.95
    }
})

</script>
<style>
.title {
        position: absolute;
        bottom: 5%;
        right: 0%;
        /* width:100%; */
        font-size: 4vw !important;
        padding-top: 3rem;
        padding-right: 1rem;
        text-align: right !important;
        color: white;
    }

.summary {
    position:absolute;
    top: 15%;
    background-color: color-mix(in srgb, var(--slidev-theme-3rd) 25%, transparent);
    width: 100%;
    padding: 2rem;
    left: 0rem;
    h1 {
        font-size: 7vw !important;
        color: white;
    }
    h2 {
        font-size: 4vw !important;
        margin-top: 3rem;
        color: var(--slidev-theme-secondary) !important;
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
    top: 30%;
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
    <div class="mask" :style="maskStyle">
    </div>
    <div class="slogan">
        {{ $slidev.nav.currentRoute.meta.slogan }}
    </div>
    <div class="seq">
        {{ $slidev.nav.currentRoute.meta.seq }}
    </div>

    <h1 class="my-auto w-full title">
        <hr style="position: absolute;top:22%">
        {{ $slidev.nav.currentRoute.meta.title }}
    </h1>
    <div class="summary">
        <slot />
    </div>
</div>
</template>
