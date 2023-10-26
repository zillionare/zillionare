<!--
  Usage:
```md
---
layout: two-cols-header
---
This spans both
::left::
# Left
This shows on the left
::right::
# Right
This shows on the right
```
-->

<script setup lang="ts">
import { computed } from 'vue'
import { handleBackground } from '../layoutHelper'

const props = defineProps({
  class: {
    type: String,
  },
  layoutClass: {
    type: String,
  },
  background: {
    default: '/public/ribbon.jpg',
  }
})

const style = computed(() => handleBackground(props.background, false))
</script>

<template>
  <div class="slidev-layout two-cols-header w-full h-full" :class="layoutClass" :style="style">
    <div class="col-header">
      <slot />
    </div>
    <div class="col-left" :class="props.class">
      <slot name="left" />
    </div>
    <div class="col-right" :class="props.class">
      <slot name="right" />
    </div>
  </div>
</template>

<style scoped>
.two-cols-header {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(5, 1fr);
}

.col-header { 
    grid-area: 1 / 1 / 2 / 3; 
}
.col-left { grid-area: 2 / 1 / 2 / 2; }
.col-right { grid-area: 2 / 2 / 5 / 3; }
</style>
