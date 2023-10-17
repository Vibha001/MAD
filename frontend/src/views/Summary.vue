<template>
  <div class="container-fluid">
    <nav
      class="navbar navbar-expand-lg navbar-light bg-light fixed-top"
      style="font-size: 24px; padding: 20px"
    >
      <h4>{{ username }}'s Dashboard</h4>
      |
      <br />
      <router-link to="/admin_dashboard"> Dashboard </router-link> |<br />
      <router-link to="/summary"> Summary </router-link> |<br />
      <LogOutButton />
    </nav>
    <img
      id="theatreSummaryImage"
      alt="Theatre Summary"
      :src="theatreSummaryImageSrc"
    />
    <img id="showSummaryImage" alt="Show Summary" :src="showSummaryImageSrc" />
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
import LogOutButton from "./Logout.vue";
export default {
  name: "Sum-mary",

  components: {
    LogOutButton,
  },
  setup() {
    const username = ref("");
    const theatreSummaryImageSrc = ref("");
    const showSummaryImageSrc = ref("");

    onMounted(async () => {
      console.log("Sumary mounted");
      const storedData = localStorage.getItem("identity");
      if (storedData) {
        const identityObject = JSON.parse(storedData);
        username.value = identityObject.username;
      }
      const response = await fetch("http://127.0.0.1:8000/theatre_summmary", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      });

      if (response.ok) {
        try {
          const responseData = await response.json();
          const imageBase64 = responseData.theatre_image_base64;
          const dataURI = `data:image/png;base64,${imageBase64}`;
          theatreSummaryImageSrc.value = dataURI;
        } catch (error) {
          console.error("Error parsing image data:", error);
        }
      } else {
        console.error(
          "Failed to fetch theater summary image. Status code:",
          response.status
        );
      }
      const showResponse = await fetch("http://127.0.0.1:8000/show_summmary", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      });

      if (showResponse.ok) {
        try {
          const showData = await showResponse.json();
          const showImageBase64 = showData.show_image_base64;
          const showDataURI = `data:image/png;base64,${showImageBase64}`;
          showSummaryImageSrc.value = showDataURI;
        } catch (error) {
          console.error("Error parsing show image data:", error);
        }
      } else {
        console.error(
          "Failed to fetch show summary image. Status code:",
          showResponse.status
        );
      }
    });

    return { username, theatreSummaryImageSrc, showSummaryImageSrc };
  },
};
</script>
