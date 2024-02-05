<template>
  <div id="app">
    <section class="upload-section">
      <input type="file" ref="fileInput" @change="fileSelected" />
      <button @click="submitFile" v-if="file">Upload File</button>
    </section>
    <section class="link-section" v-if="uuid">
      <div class="link-content">
        <p>Once your results are ready, they will be available at this link</p>
        <a :href="'https://epyc.astro.washington.edu/~avaran/' + uuid + '.html'" target="_blank" class="generated-link">Access Your Report</a>
      </div>
    </section>
    <div class="modal" v-if="showModal">
      <div class="modal-content">
        <p>Welcome to HelioLinc! To run the algorithm, choose your data and submit it. The file must be in ADES format</p>
        <p>Note that depending on the size of your file, processing can take up to five minutes.</p>
        <button @click="closeModal">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';


const file = ref(null);
const showModal = ref(true);
const uuid = ref(null);

const fileSelected = (event) => {
  file.value = event.target.files[0];
};

const closeModal = () => {
  showModal.value = false;
};

const submitFile = async () => {
  if (!file.value) {
    alert('Please select a file first.');
    return;
  }

  try {
    const formData = new FormData();
    formData.append('file', file.value);

    const response = await axios.post('/api/model/generate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    console.log(response.data);
    uuid.value = response.data.uuid;
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};

</script>

<style>
body, h1, p {
  margin: 0;
  padding: 0;
  font-family: 'Noto Sans', sans-serif;
}

#app {
  background-color: #f4f4f4;
}

nav {
  background-color: #333;
  padding: 0 20px;
}

.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-logo {
  font-size: 1.8rem;
  color: #fff;
  text-decoration: none;
}

#nav-mobile li {
  display: inline;
  margin: 0 10px;
}

#nav-mobile li a {
  color: #fff;
  text-decoration: none;
  transition: color 0.3s;
}

#nav-mobile li a:hover {
  color: #4CAF50;
}

header {
  background-color: #4CAF50;
  color: white;
  text-align: center;
  padding: 20px;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.2);
}

.info-section {
  padding: 40px 20px;
  text-align: center;
  line-height: 1.6;
  background: white;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}

.upload-section {
  text-align: center;
  padding: 20px;
  background: white;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

button:hover {
  background-color: #45a049;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  width: 80%;
  max-width: 500px;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.3);
}

.link-section {
  text-align: center;
  padding: 30px 20px;
  background: #e7ffeb;  /* Light green background for visibility */
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.link-content {
  padding: 20px;
  border: 1px solid #d1e9d6;  /* Slight border to highlight */
  border-radius: 5px;
  background: white;
}

.generated-link {
  color: #4CAF50;
  text-decoration: none;
  font-weight: bold;
  border: 2px solid #4CAF50;
  padding: 10px 20px;
  border-radius: 5px;
  display: inline-block;
  margin-top: 15px;
  transition: background-color 0.3s, color 0.3s;
}

.generated-link:hover {
  background-color: #4CAF50;
  color: white;
}
</style>
