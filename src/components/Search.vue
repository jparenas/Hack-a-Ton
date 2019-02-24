<template>
<div class="submit-all">
  <div id="target_point">It's time for an adventure!!</div>
  <div class="contents">
    <form @submit.prevent='getFormValues'>

      <div class="content">
        <label for="origin">Departure Airport: <input class="airport" name="departure" id="departure" placeholder="Enter 3 Letters" maxlength="3" style="text-transform:uppercase"> </label>
      </div>

      <div class="content">
        <label for="location">Destination Airport: <input class="airport" name="destination" id="destination" placeholder="Enter 3 Letters" maxlength="3" style="text-transform:uppercase"> </label>
      </div>

      <div class="content">
        <label for="date">Date: </label>
        <label for="date"><p class="date">From <input type="date" id="date" name="d_date" class="input_date"></p>
        <p class="date">To<input type="date" id="date" name="trip_date" class="input_date"></p></label>
      </div>

      <div class="content">
        <label for="budget">Budget: </label>
        <input type="number" id="budget" name="trip_budget" class="input_budget" placeholder="$">
      </div>

      <div class="submit-button">
        <!-- <router-link to="/search">Search</router-link> -->
        <button type="submit">Search</button>
        <!-- <input type="submit" value="Submit" class="info-submit"> -->
      </div>

    </form>
  </div>
</div>
</template>

<script lang="ts">
import ShowPage from './ShowPage.vue';

export default {
  components: {
    ShowPage
  },
  methods: {
    getFormValues (submitEvent) {
      this.$router.push('show?origin=' + submitEvent.target.elements.departure.value + "&budget=" + submitEvent.target.elements.trip_budget.value + "&start_date=" + '' + "&end_date="  + '')
    }
  }
}
</script>

<style scoped>
@import '../assets/styles/button.css';
@import '../assets/styles/text.css';
</style>
