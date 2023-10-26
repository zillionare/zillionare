
<style>
    hr {
        content: ' ';
        display: block;
        width: 98%;
        position: absolute;
        top: 10vh;
        left: 1vw;
        border-style: none;
        border-bottom-width: 1px;
        border-bottom-style: solid;
        border-image: linear-gradient(to right, var(--slidev-theme-primary) 20%, white 100%, var(--slidev-theme-primary) 0%) 1;
    }

    header:before {
        content: 'JIEYU.AI';
        position: absolute;
        right: 1vw;;
        top: 1.5vh;
        @apply text-sm;
        letter-spacing: 0.3vw;
        color: transparent;
        background: url('/public/text-clip-4.png') 80% 50% no-repeat;
        background-clip: text;
    }

    header {
        width: 100%;
        height: 2vh;
    }
</style>
<template>
  <header
    v-if="$slidev.nav.currentLayout !== 'cover' && $slidev.nav.currentLayout !== 'section' && $slidev.nav.currentLayout !== 'thanks'"
    class="absolute top-0 left-0 p-2 flex items-center"
  >
  </header>
</template>
