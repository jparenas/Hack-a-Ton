<template>
  <section class="row">
    <section class="main">
      <!-- Insert an image -->
      <div>
        <Card
          v-for="flight in info"
          v-bind:key="flight.destination"
          v-bind:destination="flight.destination"
          v-bind:imageUrl="flight.image"
        ></Card>
      </div>
      <h2 v-if="!info">Loading</h2>

      <!-- Show like and unlike buttons -->
      <div class="controls">
        <button class="button left">
          <i class="prev"></i>
          <span class="text-hidden">prev</span>
        </button>
        <button class="button right">
          <i class="next"></i>
          <span class="text-hidden">next</span>
        </button>
        <!-- <button v-on:click="dislikeHander" class="button left"><i class="prev"></i><span class="text-hidden">prev</span></button>
        <button v-on:click="likeHandler" class="button right"><i class="next"></i><span class="text-hidden">next</span></button>-->
      </div>
    </section>

    <section class="side">
      <!-- <p>{{count}} times clicked!</p> -->
      <Flight/>
    </section>
  </section>
</template>

<script>
import Flight from "./Flight.vue";
import Card from "./Card.vue";
import axios from "axios";

export default {
  name: "ShowPage",
  props: {
    msg: String
  },
  data() {
    return {
      info: null
    };
  },
  components: {
    Flight,
    Card
  },
  mounted() {
    function shuffle(a) {
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    }

    axios.defaults.withCredentials = true;
    axios
      .get(
        "http://localhost:8080/api/get_flights?end_date=2019-03-01&start_date=2019-02-24&budget=500&uuid=1&origin=MAD"
      )
      .then(response => {
        this.info = shuffle(response.data.flights);
      });
  }
  // data() {
  //   return {
  //     count: 0
  //   }
  // },
  // methods: {
  //   likeHandler: function(event) {
  //     this.count++,
  //     console.log(this.count)
  //   },
  //   dislikeHander: function(event) {
  //     this.count++,
  //     console.log(this.count)
  //   },
  //   removeElement: function (index) {
  //     this.items.splice(index, 1);
  //   }
  // }
};
</script>

<style scoped>
p {
  color: white;
}
@import "../assets/styles/showpage.css";
@import "../assets/styles/button.css";

.button {
  border: solid;
  border-width: 2px;
  bottom: 10px;
}

.main {
  height: 100%;
}
</style>
