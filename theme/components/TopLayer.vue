<script setup lang="ts">
import { computed } from 'vue'
import { parseRangeString } from '@slidev/parser/core'

const props = defineProps({
    top: {
        type: String,
        default: "0"
    },
    left: {
        type: String,
        default: "0"
    },
    hcenter: {
        type: Boolean,
        default: false
    },
    vcenter: {
        type: Boolean,
        default: false
    },
    center: {
        type: Boolean,
        default: false
    },
    fc: {
        type: String,
        default: "rgba(255, 255, 255, 0.88)"
    },  
    at: {
    required: true
  }
})

const show = computed(() => {
    var at = props.at
    if (at === undefined){
        return false
    }

    if (typeof(at) === "number") {
        at = String(at)
    }

    var ranges = parseRangeString(10, at)
    return ranges.includes($slidev.nav.clicks)
})

const style = computed(() => {
    var s = {
        "position": "fixed",
        "top": props.top,
        "left": props.left,
        "width": "100%",
        "height": "100%",
        "background-color": props.fc,
        "z-index": "999"
    }

    if (props.vcenter){
        s["display"] = "flex"
        s["align-items"] = "center"
    }

    if (props.hcenter){
        s["display"] = "flex"
        s["justify-content"] = "center"
    }

    if (props.center){
        s["display"] = "flex"
        s["justify-content"] = "center"
        s["align-items"] = "center"
    }
    return s
})

</script>
<template>
    <div v-if="show" :style="style"><slot /></div>
</template>
