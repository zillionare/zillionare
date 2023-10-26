<script setup>
import { onMounted } from 'vue'
import { useScriptTag } from '@vueuse/core'
import $ from 'jquery'
window.$ = $;

onMounted(()=>{
    function autoType(elementClass, typingSpeed){
        var thhis = $(elementClass);
        thhis.css({
            "position": "relative",
            "display": "inline-block"
        });
        thhis.prepend('<div class="cursor" style="right: initial; left:0;"></div>');
        thhis = thhis.find(".text-js");
        var text = thhis.text().trim().split('');
        var amntOfChars = text.length;
        var newString = "";
        thhis.text("|");
        setTimeout(function(){
            thhis.css("opacity",1);
            thhis.prev().removeAttr("style");
            thhis.text("");
            for(var i = 0; i < amntOfChars; i++){
            (function(i,char){
                setTimeout(function() {        
                newString += char;
                thhis.text(newString);
                },i*typingSpeed);
            })(i+1,text[i]);
            }
        },1500);
    }
    autoType(".type-js",200);
})
</script>

<template>
<div class="wrapper">
    <div class="type-js headline">
        <h1 class="text-js">repeat </h1>
    </div>
</div>
</template>
<style scoped>
.text-js{
  opacity: 0;
}
.cursor{
  display: block;
  position: absolute;
  height: 100%;
  top: 0;
  right: -5px;
  width: 2px;
  /* Change colour of Cursor Here */
  background-color: white;
  z-index: 1;
  animation: flash 0.5s none infinite alternate;
}
@keyframes flash{
  0%{
    opacity: 1;
  }
  100%{
    opacity: 0;
  }
}
</style>
