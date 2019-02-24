<template>
<div id='container'>
	<div>
		<img id='destination_image' v-bind:src='imageUrl' width=750px/>
	</div>
	<div>
		<h2>{{destination}}</h2>
	</div>
</div>
</template>

<script>
export default {
	name: 'Card',
	props:{
		destination: String,
		imageUrl: String,
	},
	data () {
		return {

		}
	}
}
</script>

<style scoped>
#container {
background: GRAY;
border-style:solid;
}
</style>