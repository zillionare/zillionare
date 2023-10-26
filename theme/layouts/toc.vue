<!-- 课程大纲，由一个mindmap图构成 -->

<script setup>
import { computed } from 'vue'

const props = defineProps({
  image: {
    type: String,
    required: true,
  },
  imageOrder: {
    type: Number,
    default: 1
  }
})
</script>

<template>
  <div class="slidev-layout h-full grid">
    <h1 style="margin-bottom: 0px">课程内容</h1>
    <hr/>

    <div class="h-100 flex justify-center items-center  object-contain" :class="imageOrder">
        <img :src="image" class="rounded-2xl border-image h-full object-contain" />
    </div>

    <div style="position: absolute; height:100%; width:100%">
        <slot />
    </div>

  </div>
</template>
