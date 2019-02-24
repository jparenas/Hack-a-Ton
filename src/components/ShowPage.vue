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
        <button v-on:click="like('left')" class="button left">
          <i class="prev"></i>
          <span class="text-hidden">prev</span>
        </button>
        <button v-on:click="like('right')" class="button right">
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
      <Liked
        v-for="item in liked"
        v-bind:key="item.destination"
        v-bind:destination="item.destination"
        v-bind:liked="item.liked"
      ></Liked>
    </section>
  </section>
</template>

<script>
import Flight from "./Flight.vue";
import Card from "./Card.vue";
import Liked from "./Liked.vue";
import axios from "axios";
import { uuid } from 'vue-uuid';

export default {
  name: "ShowPage",
  props: {
    origin: String,
  },
  data() {
    return {
      info: null,
      liked: [],
      uuid: uuid.v1(),
      //uuid:  String(this.$uuid.v5().v5.DNS)
    };
  },
  components: {
    Flight,
    Card,
    Liked
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
        "/api/get_flights?end_date=2019-03-01&start_date=2019-02-24&budget=500&uuid=" + this.uuid + "&origin=" + this.origin
      )
      .then(response => {
        this.info = shuffle(response.data.flights);
      });
  },
  methods: {
    like: function (side) {
      var is_like;
      if (side === "left") {
        is_like = false
      } else {
        is_like = true
      }

      if (this.info.length > 0) {
        var removed_entry = this.info.shift()
        removed_entry.liked = is_like

        axios
        .post(
            "/api/like_place", {
            uuid: this.uuid,
            like: is_like,
            destination: removed_entry.destination,
          }
        )
        .then(response => {
          this.liked.push(removed_entry);
        });
      }

    }
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
