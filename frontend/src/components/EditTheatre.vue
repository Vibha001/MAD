<template>
  <div>
    <button
      type="button"
      class="btn btn-outline-secondary rounded-pill"
      data-bs-toggle="modal"
      :data-bs-target="'#staticBackdropEditTheatre' + id"
    >
      Edit Theatre
    </button>
    <!-- Add Show Modal -->
    <div
      :id="'staticBackdropEditTheatre' + id"
      class="modal fade"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      :aria-labelledby="'staticBackdropEditTheatreLabel' + id"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" :id="'staticBackdropEditTheatreLabel' + id">
              Edit Theatre
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
              <label> Name of the Theatre : </label>
              <input required v-model="showData.name" type="text" />
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
  name: "EditTheatre",
  props: {
    id: Number,
  },
  data() {
    return {
      showData: {
        name: "",
      },
    };
  },
  methods: {
    saveChanges() {
      // Emit the 'addShow' event with the added show data
      this.$emit("editTheatre", this.id, this.showData.name);

      // Clear the input fields after emitting the event
      this.showData = {
        name: "",
      };
    },
  },
};
</script>
