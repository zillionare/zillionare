<!-- https://blog.stackfindover.com/javascript-text-animation-examples/ -->
<script setup lang="ts">
import { computed} from 'vue'

const props = defineProps({
    text: {
        type: String
    },
    top: {
        type: String,
        default: "0",
    },
    left: {
        type: String,
        default:"0"
    },
    width: {
        type: String,
        default: "100%"
    },
    height: {
        type: String,
        default: "10%"
    },
    color: {
        type: String,
        default: 'color: rgb(255,255,255)'
    },
    bcolor: {
        type: String,
        default: 'azure'
    }
})

const style = computed(()=>{
    return {
        "top": props.top,
        "left": props.left,
        "width": props.width,
        "height": props.height,
        "color": props.color
    }
})

const words = computed(() =>{
    let groups = props.text?.replaceAll(" ", "  ").split("|")
    return groups
})

</script>

<template>
    <div class="container" :style="style">
        <div v-for="(word, i) in words" >
            <div class="words">
                <span v-for="letter in word"> {{ letter }}</span>
            </div>
        </div>
    </div>
</template>

<style>
.container {
    font-family: "WenQuanYi MicroHei", sans-serif;
    /* background: #f4d03f; */
    position: absolute;
    text-align: center;
}

.words {
    /* color: #f4d03f; */
    /* font-size: 0; */
    line-height: 1.5;
}

.words span {
    display: inline-block;
    animation: move 3s ease-in-out infinite;
    margin: 0 3px;
}

@keyframes move {
  0% {
    transform: translate(-30%, 0);
    color: var(--slidev-back-ground-color);
  }
  50% {
    text-shadow: 0 25px 50px rgba(0, 0, 0, 0.75);
    color: var(--slidev-theme-primary);
  }
  100% {
    transform: translate(30%, 0);
    color: var(--slidev-back-ground-color);
  }
}

.words span:nth-child(2) {
  animation-delay: 0.5s;
}

.words span:nth-child(3) {
  animation-delay: 1s;
}

.words span:nth-child(4) {
  animation-delay: 1.5s;
}

.words span:nth-child(5) {
  animation-delay: 2s;
}

.words span:nth-child(6) {
  animation-delay: 2.5s;
}

.words span:nth-child(7) {
  animation-delay: 3s;
}

.words span:nth-child(8) {
  animation-delay: 3.5s;
}

.words span:nth-child(9) {
  animation-delay: 4s;
}

.words span:nth-child(10) {
  animation-delay: 4.5s;
}
</style>
