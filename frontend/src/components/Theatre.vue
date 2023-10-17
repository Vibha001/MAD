<template>
  <div>
    <div class="row">
      <AddTheatre @addT="addTheatre" />
      <div
        class="card col-5 my-4 mx-4"
        style="width: 18rem"
        v-for="(venue, venueId) in venues"
        :key="venueId"
      >
        <div class="card-body">
          <h5 class="card-title">{{ venue.vname }}</h5>
          <img
            :src="'http://localhost:8000' + venue.vimage_url"
            alt="Venue Image"
          /><br /><br />

          <h6 class="card-subtitle mb-2 text-muted">
            Location: {{ venue.vplace }}
          </h6>
          <h6 class="card-subtitle mb-2 text-muted">
            Capacity: {{ venue.vcapacity }}
          </h6>
          <div
            class="my-4 mx-4 border border-2 border-secondary rounded-3"
            v-for="(show, showId) in venue.shows"
            :key="showId"
          >
            <h6 class="card-subtitle mb-2 text-muted">
              Show Name: {{ show.sname }}
            </h6>
            <p class="card-text">Tags: {{ show.stags }}</p>
            <p class="card-text">Ticket Price: {{ show.sprice }}</p>
            <p class="card-text">Show Timing: {{ show.time }}</p>
            <p class="card-text">Number of Seats: {{ show.seats }}</p>
            <p class="card-text">Number of Seats Booked: {{ show.booked }}</p>
            <EditShowModal
              :id="show.sid"
              :name="show.vname"
              @editShow="editShow"
            /><br />
            <button
              type="button"
              class="btn btn-outline-danger rounded-3"
              @click="delSh(show.sid)"
            >
              Delete Show</button
            ><br />
            <p></p>
          </div>
          <br />
          <AddShowVue
            :id="Number(venueId)"
            :name="venue.vname"
            :tags="venue.vtags"
            :price="venue.vprice"
            :seats="venue.vseats"
            :timing="venue.vtiming"
            @addShow="addShow"
          />

          <br />
          <EditTheatreVue
            :id="Number(venueId)"
            :name="venue.vname"
            @editTheatre="editTh"
          /><br />
          <button
            type="button"
            class="btn btn-outline-danger rounded-3"
            @click="delTh(venueId)"
          >
            Delete Theatre
          </button>
          <br />
          <br />
          <button
            class="btn btn-outline-secondary border border-2 rounded-pill"
            @click="export_csv(venueId)"
          >
            Export
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AddShowVue from "./AddShow.vue";
import EditTheatreVue from "./EditTheatre.vue";
import EditShowModal from "./EditShow.vue";
import AddTheatre from "./AddTheatre.vue";

export default {
  name: "VenueList",
  components: {
    EditTheatreVue,
    AddShowVue,
    EditShowModal,
    AddTheatre,
  },
  data: function () {
    return {
      venues: [],
      showData: {
        name: "",
        tags: "",
        price: "",
        timing: "",
        seats: "",
        image: null,
      },
    };
  },
  methods: {
    addTheatre(theatreData) {
      const formData = new FormData();
      formData.append("name", theatreData.name);
      formData.append("location", theatreData.loc);
      formData.append("capacity", theatreData.cap);
      formData.append("image", theatreData.image);

      fetch("http://127.0.0.1:8000/newTheatre", {
        method: "POST",
        body: formData,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to add theatre. Server returned an error.");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Theatre added:", data);

          // Fetch updated data after adding a theatre
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
            .then((response) => response.json())
            .then((data) => {
              console.log(
                "Data fetched from the backend after adding theatre:",
                data
              );
              this.venues = data; // Assuming `venues` is part of your data
            });
        })
        .catch((error) => {
          console.error("Error while adding theatre:", error);
        });
    },

    delTh: function (id) {
      console.log(id);
      fetch(`http://127.0.0.1:8000/deleteTheatre/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Unsupported Media Type");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Theatre Deleted:", data);
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
            .then((response) => response.json())
            .then((data) => {
              console.log("from backend", data);
              this.venues = data;
              // this.$router.go(0);
            });
        });
    },
    export_csv: function (vid) {
      console.log("Export ", vid);

      // Fetch the data first
      fetch(`http://127.0.0.1:8000/get_th_data/${vid}`)
        .then((response) => response.json())
        .then((data) => {
          console.log("Task details", data);

          // After fetching the data, trigger the download
          fetch(`http://127.0.0.1:8000/download_file/${vid}`)
            .then((response) => {
              if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
              }
              return response.blob(); // Get the response as a Blob
            })
            .then((blob) => {
              // Create a URL for the Blob
              const url = window.URL.createObjectURL(blob);

              // Create an anchor element
              const a = document.createElement("a");
              a.href = url;
              a.download = `th_data_${vid}.csv`;

              // Simulate a click event on the anchor element
              a.click();

              // Clean up by revoking the Blob URL
              window.URL.revokeObjectURL(url);
            })
            .catch((error) => {
              console.error("Fetch error:", error);
            });
        })
        .catch((error) => {
          console.error("Fetch error:", error);
        });
    },

    delSh: function (id) {
      console.log(id);
      fetch(`http://127.0.0.1:8000/deleteShow/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Unsupported Media Type");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Show added:", data);
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
            .then((response) => response.json())
            .then((data) => {
              console.log("from backend", data);
              this.venues = data;
              // this.$router.go(0);
            });
        });
    },
    editShow: function (ShId, editedShowData) {
      console.log("Show edited", ShId, editedShowData);
      const data = {
        sname: editedShowData,
      };
      fetch(`http://127.0.0.1:8000/editShow/${ShId}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Show edited:", data);
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
            .then((response) => response.json())
            .then((data) => {
              console.log("from backend", data);
              this.venues = data;
              // this.$router.go(0);
            });
        });
    },
    editTh: function (id, editedTheatreName) {
      console.log("Theatre edited", id);
      const data = { name: editedTheatreName };
      console.log(JSON.stringify(data));
      fetch(`http://127.0.0.1:8000/editTheatre/${id}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Unsupported Media Type");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Show added:", data);
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
            .then((response) => response.json())
            .then((data) => {
              console.log("from backend", data);
              this.venues = data;
              // this.$router.go(0);
            });
        });
    },
    addShow({ id, showData }) {
      console.log("Show added to Theatre", id);
      const data = {
        name: showData.name,
        tags: showData.tags,
        price: showData.price,
        timing: showData.timing,
        seats: showData.seats,
        booked: 0,
        rate: 0,
      };

      fetch(`http://127.0.0.1:8000/addShow/${id}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Unsupported Media Type");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Show added:", data);
          const options = {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("token"),
            },
          };
          fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
            .then((response) => response.json())
            .then((data) => {
              console.log("from backend", data);
              this.venues = data;
              // this.$router.go(0);
            });
        });
    },
  },
  mounted: function () {
    const options = {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    };
    fetch("http://127.0.0.1:8000/getVenuesAndShows", options)
      .then((response) => response.json())
      .then((data) => {
        console.log("Venues and Shows data from backend", data);
        this.venues = data;
      });
  },
};
</script>
