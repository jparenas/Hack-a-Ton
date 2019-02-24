<template>
  <div id="app">
  <!--   <Select/> -->
  <Airports/>
  </div>
</template>

<!-- script type="text/javascript" src="https://cdn.jsdelivr.net/jquery/latest/jquery.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" /> -->

<script>
// import Select from './components/Select.vue'
import Airports from './components/Airports.vue'
export default {
  name: "Airports",
  components: {
  //Select
  Airports
  }
}

</script>

  <style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  @import './assets/styles/button.css';
  @import './assets/styles/text.css';
  </style>
