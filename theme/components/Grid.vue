<!--<style>
 .container {
    position: absolute;
    width: 100%;
    height: 100%;
}
.about {
    position: absolute;
    top: 0vh;
    left: 50%;
    padding: 10px;
    color: red;
    width: 150px;
    height: 2rem;
}
</style>

<script setup>
import {ref, reactive, onMounted} from 'vue'

function MouseMovement(){
	const movement = reactive({x:window.pageXOffset, y:window.pageYOffset});
	onMounted(()=>{
		window.addEventListener("mousemove",function(e){
            const parent = document.getElementById("slide-content").getBoundingClientRect();
            
			movement.x = e.pageX - parent.x;
			movement.y = e.pageY - parent.y;
		})
	})

	return movement;
}

const mouse = MouseMovement()
</script>

<template>
<div class="container">
  <div class="about">
	<span>x: {{Math.round(mouse.x,0)}},y: {{Math.round(mouse.y,0)}}</span>
	 
  </div>
</div>
</template>-->
<style>
.container {
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.row {
    width: 100%;
    height: 10%;
    display: flex;
    margin: 0;
    padding: 0;
}

.col {
    height: 100%;
    width: 10%;

    border: 1px dashed grey;
    margin: 0;
    padding: 0;
    font-size: 20px;
    color: black;
    opacity: 0%;
}

.col:hover {
    opacity: 100%;
}

</style>

<template>
    <!-- Grid -->
    <div class="container">
        <div v-for = "i in 10" class="row">
            <div v-for = "j in 10" class="col" >
                top: {{ (i - 1) * 10}}% left: {{ (j - 1) * 10}}%
        </div>
        </div>
    </div>
</template>
