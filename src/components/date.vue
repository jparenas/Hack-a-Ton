<template>
	<div id = 'datecheckerapp'>
		<div>
			<h3>datepicker</h3>
			<datepicker placeholder="Select Date" v-model="vModelExample"></datepicker>
		</div>
	</div>
</template>

<script>
import Datepicker from "vuejs-datepicker/dist/vuejs-datepicker.esm.js";
import * as lang from "vuejs-datepicker/src/locale";

export default {
	name: "datecheckerpp",
  	components: {
    	Datepicker
  	},
  	format: "MM/DD/YYYY"

}
</script>

