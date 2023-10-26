<script setup>
import { computed } from 'vue'
import { parseRangeString } from '@slidev/parser/core'

const props = defineProps({
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

</script>
<template>
  <div v-if = "show">
      <slot />
  </div>
</template>
