<style>
.box:hover {
    opacity: 100% !important;
}

.box{
    border-radius: 10px;
    border-width: 3px;
    box-shadow: 3px 3px rgba(0,0,0,0.3);
    opacity: 0%;
    transition-duration: 1s;
}
</style>

<script setup lang="ts">
import { computed} from 'vue'
import { parseRangeString } from '@slidev/parser/core'

const props = defineProps({
    position: {
        type: String,
        default: "absolute"
    },
    top: {
        type: String,
        default: "50%"
    },
    left: {
        type: String,
        default: "50%"
    },
    color: {
        type: String,
        default: "#ff0000",
    },
    lw: {
        type: String,
        default: "3px"
    },
    d: {
        type: Boolean
    },
    w: {
        type: String,
        default: "200px",
    },
    h: {
        type: String,
        default: "2.5rem"
    },
    at: {
        type: String
    }
})

const style = computed(()=>{
    let style = {
        "height": props.h,
        "width": props.w,
        "position": props.position,
        "top": props.top,
        "left": props.left,
        "border-color": props.color,
        "border-width": props.lw,
        "opacity": 0
    }
    if (props.d){
        style["opacity"] = 0.8
    }

    if (props.at){
        style["opacity"] = 0.8
    }
    return style
})

const show = computed(() => {
    var at = props.at
    if (at === undefined){
        return true
    }

    if (typeof(at) === "number") {
        at = String(at)
    }

    var ranges = parseRangeString(10, at)
    return ranges.includes($slidev.nav.clicks)
})

</script>
<template>
    <!-- Box -->
    <div v-if="show" class="box" :style="style">&nbsp</div>
</template>
