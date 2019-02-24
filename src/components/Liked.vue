<template>
    <div>
        <h3>{{destination}} - {{price}} <span v-if="liked">⭐</span></h3>
    </div>
</template>

<script>
export default {
    name: "Liked",
    props: {
        destination: String,
        price: String,
        super_liked: Boolean,
        liked: Boolean
    },
    data() {
        return {};
    }
}
</script>

<style scoped>

</style>
