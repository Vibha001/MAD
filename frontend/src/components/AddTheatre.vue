<template>
  <div>
    <button
      type="button"
      class="btn btn-outline-success btn-lg rounded-3"
      data-bs-toggle="modal"
      data-bs-target="#staticBackdropAddTheatre"
    >
      Add Theatre
    </button>
    <div>
      <!-- Button trigger modal -->
      <div
        id="staticBackdropAddTheatre"
        class="modal fade"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="staticBackdropLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="staticBackdropLabel">Add Theatre</h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="my-4">
                <label>Name of the Theatre :</label>
                <input v-model="showData.name" type="text" required />
              </div>
              <div class="my-4">
                <label>Location of Theatre :</label>
                <input v-model="showData.loc" type="text" required />
              </div>
              <div class="my-4">
                <label>Capacity of Theatre :</label>
                <input v-model="showData.cap" type="text" required />
              </div>
              <div class="my-4">
                <label>Upload Theatre View Image :</label>
                <input
                  type="file"
                  @change="handleImageUpload"
                  accept="image/*"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button
                type="button"
                @click="saveChanges"
                class="btn btn-primary"
                data-bs-dismiss="modal"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddTheatre",
  data() {
    return {
      showData: {
        name: "",
        loc: "",
        cap: "",
        image: null,
      },
    };
  },
  methods: {
    saveChanges() {
      // Emit the 'addShow' event with an object containing both id and showData
      this.$emit("addT", this.showData);

      //   this.$emit("addT", {
      //     showData: {
      //       name: this.showData.name,
      //       cap: this.showData.cap,
      //       loc: this.showData.loc,
      //       image: this.showData.image,
      //     },
      //   });

      // Clear the input fields after emitting the event
      this.showData = {
        name: "",
        loc: "",
        cap: "",
        image: null,
      };
    },
    handleImageUpload(event) {
      // Handle the image upload and store it in the 'showData' object
      this.showData.image = event.target.files[0];
    },
  },
};
</script>
