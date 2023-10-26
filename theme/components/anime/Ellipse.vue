<style>
.ellipse:hover {
    opacity: 100%;
}

.ellipse{
    border-radius: 50%;
    border-width: 5px;
    box-shadow: 3px 3px rgba(0,0,0,0.2);
    opacity: 0%;
    transition-duration: 1s;
}
</style>

<script setup lang="ts">
import { computed} from 'vue'

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
    s: {
        type: Number,
        default: 200,
    },    
    at: {
        type: String
    }
})

const style = computed(()=>{
    let style = {
        "height": props.s / 2 + "px",
        "width": props.s + "px",
        "position": props.position,
        "top": props.top,
        "left": props.left,
        "border-color": props.color,
        "border-width": props.lw,
        "z-index": 999
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
    <!-- Ellipse -->
    <div v-if="show" class="ellipse" :style="style"></div>
</template>
