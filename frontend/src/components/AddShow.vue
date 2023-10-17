<template>
  <div>
    <button
      type="button"
      class="btn btn-outline-success rounded-3"
      data-bs-toggle="modal"
      :data-bs-target="'#staticBackdropAddShow' + id"
    >
      Add Show
    </button>
    <!-- Add Show Modal -->
    <div
      :id="'staticBackdropAddShow' + id"
      class="modal fade"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      :aria-labelledby="'staticBackdropAddShowLabel' + id"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" :id="'staticBackdropAddShowLabel' + id">
              Add Show
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="my-4">
              <label> Name of the Show : </label>
              <input required v-model="showData.name" type="text" />
            </div>
            <div class="my-4">
              <label> Tags : </label>
              <input required v-model="showData.tags" type="text" />
            </div>
            <div class="my-4">
              <label> Ticket Price : </label>
              <input required v-model="showData.price" type="text" />
            </div>
            <div class="my-4">
              <label> Show Timing : (Format : HH:MM:SS) </label>
              <input required v-model="showData.timing" type="text" />
            </div>
            <div class="my-4">
              <label> Number of seats : </label>
              <input required v-model="showData.seats" type="text" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>
            <button
              type="button"
              @click="saveChanges"
              class="btn btn-primary"
              data-bs-dismiss="modal"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddShow",
  props: {
    id: Number,
    name: String,
    tags: String,
    price: String,
    timing: String,
    seats: String,
  },
  data() {
    return {
      showData: {
        name: "",
        tags: "",
        price: "",
        timing: "",
        seats: "",
      },
    };
  },
  methods: {
    saveChanges() {
      // Emit the 'addShow' event with an object containing both id and showData
      this.$emit("addShow", {
        id: this.id,
        showData: {
          name: this.showData.name,
          tags: this.showData.tags,
          price: this.showData.price,
          timing: this.showData.timing,
          seats: this.showData.seats,
        },
      });

      // Clear the input fields after emitting the event
      this.showData = {
        name: "",
        tags: "",
        price: "",
        timing: "",
        seats: "",
      };
    },
  },
};
</script>
