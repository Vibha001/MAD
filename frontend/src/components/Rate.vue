<template>
  <div>
    <div class="star-rating">
      <span
        v-for="star in maxStars"
        :key="star"
        @click="setRating(star)"
        :class="{ filled: star <= selectedRating }"
      >
        &#9733;
      </span>
      <button @click="rate" class="btn btn-outline-secondary">Rate</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Ra-te",
  props: {
    value: Number, // Use "value" prop for v-model
    maxStars: Number,
  },
  data() {
    return {
      selectedRating: this.value || 0,
    };
  },
  methods: {
    setRating(rating) {
      this.selectedRating = rating;
    },
    rate() {
      this.$emit("update:value", this.selectedRating); // Emit "update:value" event
      this.$emit("rate", this.selectedRating); // Emit "rate" event
    },
  },
};
</script>

<style scoped>
.star-rating {
  display: inline-block;
}

.star-rating span {
  font-size: 24px;
  cursor: pointer;
}

.star-rating span.filled {
  color: gold;
}
</style>
