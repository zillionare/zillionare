<style>
    footer {
        color: #bebebe;
        z-index: 999;
    }
</style>
<template>
  <footer class="absolute bottom-0 left-5 p-2 text-3xl"><br/><SlideCurrentNo/>/<SlidesTotal/></footer>
  <footer
    v-if="$slidev.nav.currentLayout !== 'cover'"
    class="absolute bottom-0 right-0 p-2 flex items-center"
  >
    <span style="font-size:3vw">@quantfans_99 (宽粉)</span>
  </footer>
</template>
