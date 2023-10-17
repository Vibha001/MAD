<template>
  <div>
    <button
      type="button"
      class="btn btn-outline-success rounded-3"
      data-bs-toggle="modal"
      :data-bs-target="'#staticBackdropBook' + id"
    >
      Book Now
    </button>
    <div
      :id="'staticBackdropBook' + id"
      class="modal fade"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      :aria-labelledby="'staticBackdropBookLabel' + id"
      aria-hidden="true"
    >
      <!-- Existing modal content -->
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" :id="'staticBackdropAddShowLabel' + id">
              Booking - {{ show.sname }} {{ venue.vname }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <!-- Placeholder for existing modal content -->
            <!-- ... (your existing modal content here) ... -->

            <p>Timing: {{ show.time }}</p>
            <p>Available seats: {{ show.seats - show.booked }}</p>
            <label for="numberOfSeats">Number of Seats:</label>
            <input
              type="number"
              id="numberOfSeats"
              v-model="numberOfSeats"
              min="1"
              :max="availableSeats"
            />
            <p>Price: {{ show.sprice }}</p>
            <p>Total: {{ total }}</p>
          </div>
          <div class="modal-footer">
            <!-- Confirm Booking Button -->
            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="confirmBooking"
              :disabled="numberOfSeats <= 0 || numberOfSeats > availableSeats"
            >
              Confirm Booking
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "bo-ok",
  props: {
    id: Number,
    show: Object,
    venue: Object,
  },
  data() {
    return {
      numberOfSeats: "",
    };
  },
  computed: {
    availableSeats() {
      return this.show.seats - this.show.booked;
    },
    total() {
      return this.show.sprice * this.numberOfSeats;
    },
  },
  methods: {
    confirmBooking() {
      if (this.numberOfSeats <= this.availableSeats) {
        const bookingData = {
          showId: this.show.sid,
          venueId: this.venue.vid,
          numberOfSeats: this.numberOfSeats,
          price: this.show.sprice * this.numberOfSeats,
        };
        this.$emit("booking-confirmed", bookingData);
      } else {
        alert("No available seats for the selected quantity.");
      }
    },
  },
};
</script>
