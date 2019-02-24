// forked from FumioNonaka's "Vue.js + ES6: Wrapper component using jQuery plugin Select2" http://jsdo.it/FumioNonaka/8v2v
Vue.component('select2', {
	props: {
		options: Array,
		value: Array  // Number
	},
	template: '#select2-template',
	mounted() {
		const select = $(this.$el);
		// $(this.$el)
		select
		// init select2
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
});
// import * as statename from '../src/assets/states_titlecase.json';
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script type="text/javascript" src="../src/assets/airports.json"></script>
var local_airport = airports;a
console.log(local_airport);
var vm = new Vue({
	template: '#demo-template',
	data: {
		options:[
	
			{id: "AL", text: 'Alabama'},
			{id: "AK", text: 'Alaska'},
			{id: "AZ", text: 'Arizona'}
		]
	}
});
document.addEventListener('DOMContentLoaded', (event) =>
	vm.$mount('#demo')
);




