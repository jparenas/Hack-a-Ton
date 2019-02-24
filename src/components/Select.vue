<template>
</template>

<script>
export default {
	components: {
		select2
	},
	props: {
			options: Array,
			value: Array  // Number
	},
	template: '#select2-template',
	mounted() {
		const select = $(this.$el);
		select
		.select2({data: this.options})
		.val(this.value)
		.on('change', (event) => {
			const selecions = select.select2('data')
			.map((element) => parseInt(element.id, 10));
			// this.$emit('input', parseInt(event.target.value, 10))
			this.$emit('input', selecions);
		})
		.trigger('change');
	}
}

var vm = new Vue({
	template: '#demo-template',
	data: {
		options:[
		{id: "AL", text: 'Alabama'},
		{id: "AK", text: 'Alaska'},
		{id: "AZ", text: 'Arizona'}
		]}});
document.addEventListener('DOMContentLoaded', (event) => vm.$mount('#demo'));
</script>

<style>
</style>
