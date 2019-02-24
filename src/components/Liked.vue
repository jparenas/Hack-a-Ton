<template>
    <div>
        <h3>{{destination}} - <span v-if="liked">Liked!</span><span v-else>Not liked:( RIP<span></h3>
    </div>
</template>

<script>
export default {
    name: "Liked",
    props: {
        destination: String,
        liked: Boolean
    },
    data() {
        return {};
    }
}
</script>

<style scoped>

</style>
