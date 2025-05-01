<template>
  <div class="csv-summary-container">
    <h2>CSV Summary Processing</h2>
    <div
      class="drop-zone"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      :class="{ 'drag-over': isDragging }"
    >
      <div class="file-list">
        <div v-if="file1" class="file-list-item">
          <span class="file-name">
            File 1: <strong>{{ file1.name }}</strong>
          </span>
          <button @click="removeFile(1)" class="remove-button">Remove</button>
        </div>
        <hr v-if="file1 && file2" class="file-separator" />
        <div v-if="file2" class="file-list-item">
          <span class="file-name">
            File 2: <strong>{{ file2.name }}</strong>
          </span>
          <button @click="removeFile(2)" class="remove-button">Remove</button>
        </div>
      </div>

      <p v-if="filesAttachedCount === 0" class="drop-message">
        {{ isDragging ? "¡Drop Now!" : "Drop your files here..." }}
      </p>
      <p v-else-if="filesAttachedCount === 1" class="drop-message">
        {{ isDragging ? "¡Drop Now!" : "Drop another file here..." }}
      </p>
    </div>
    <p v-if="dropError" class="error-text">{{ dropError }}</p>
    <div v-if="filesAttachedCount === 2" class="submit-section">
      <p>Ready to process</p>
      <div class="action-buttons-container">
        <button
          @click="handleSubmit"
          :disabled="isUploading"
          class="base-button submit-button"
        >
          {{ isUploading ? "Processing..." : "Process Files" }}
        </button>
        <a
          v-if="downloadUrl"
          :href="downloadUrl"
          download="test_summary.csv"
          class="base-button download-button"
        >
          Download File
        </a>
      </div>
    </div>
    <div v-if="uploadError" class="error-text">Error: {{ uploadError }}</div>
    <div v-if="succesMsg" class="success-message">{{ succesMsg }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const isDragging = ref(false);
const file1 = ref(null);
const file2 = ref(null);

const dropError = ref("");

const filesAttachedCount = computed(() => {
  let count = 0;
  if (file1.value) count++;
  if (file2.value) count++;
  return count;
});

const isUploading = ref(false);
const uploadError = ref("");
const downloadUrl = ref("");
const successMsg = ref("");

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function handleDrop(event) {
  isDragging.value = false;
  dropError.value = "";
  const files = event.dataTransfer.files;

  if (!files || files.length === 0) {
    return;
  }

  console.log("Files dropped:", files);

  let localDropError = "";

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    if (file1.value && file2.value) {
      localDropError = "Only two CSV files are allowed.";
      break;
    }
    if (file.type !== "text/csv") {
      localDropError = `Only CSV files are allowed. ${file.name} is not a CSV file.`;
      break;
    }

    const isDuplicate =
      (file1.value && file1.value.name === file.name) ||
      (file2.value && file2.value.name === file.name);
    if (isDuplicate) {
      localDropError = `Duplicate file detected: ${file.name}`;
      continue;
    }

    if (file1.value === null) {
      file1.value = file;
    } else if (file2.value === null) {
      file2.value = file;
    } else {
      localDropError = "Only two CSV files are allowed.";
      break;
    }
  }

  if (localDropError) {
    dropError.value = localDropError;
  }
}

function removeFile(fileNumber) {
  if (fileNumber == 1) {
    file1.value = null;
  } else if (fileNumber == 2) {
    file2.value = null;
  }
  dropError.value = "";
  downloadUrl.value = "";
  uploadError.value = "";
}

async function handleSubmit() {
  if (filesAttachedCount.value !== 2) {
    dropError.value = "Please attach two CSV files.";
    return;
  }
  isUploading.value = true;
  uploadError.value = "";
  downloadUrl.value = "";
  successMsg.value = "";

  const csrfToken = getCookie("csrftoken");

  if (!csrfToken) {
    uploadError.value = "CSRF token not found. Reload the page.";
    isUploading.value = false;
    return;
  }

  const formData = new FormData();
  formData.append("file1", file1.value);
  formData.append("file2", file2.value);

  console.log("Submitting files:", file1.value, file2.value);

  try {
    const response = await fetch("api/csv/upload/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(
        data.error || `Error ${response.status}: ${response.statusText}`
      );
    }

    console.log("Files uploaded successfully:", data);

    successMsg.value = `Files processed successfully!`;
    downloadUrl.value = `${data.download_url}`;
  } catch (error) {
    console.error("Error during file upload:", error);
    uploadError.value =
      error.message || "An error occurred while uploading the files.";
  } finally {
    isUploading.value = false;
  }
}
</script>

<style scoped>
.csv-summary-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.drop-zone {
  border: 3px dashed #ccc;
  padding: 1.5rem;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  border-radius: 10px;
  background-color: #f8f9fa;
  transition: background-color 0.3s ease, border-color 0.3s ease;
  min-height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

.drop-zone.drag-over {
  background-color: #e0f2f7;
  border-color: #007bff;
}

.file-list {
  width: 100%;
  margin-bottom: 1rem;
}

.file-list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  text-align: left;
}

.file-separator {
  border: none;
  border-top: 1px solid #ddd;
  margin: 0;
}

.file-name {
  font-size: 0.95rem;
  word-break: break-all;
  padding-right: 10px;
}

.remove-button {
  background: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  line-height: 20px;
  cursor: pointer;
  padding: 0;
  text-align: center;
  flex-shrink: 0;
  padding-inline: 0.5rem;
  padding-block: 0.25rem;
}
.remove-button:hover {
  background: #cc0000;
}

.drop-guidance {
  margin-top: 1rem;
  color: #6c757d;
  font-style: italic;
}
.drop-zone.drag-over .drop-guidance {
  color: #0056b3;
  font-weight: bold;
}

.drop-error-margin {
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}
.error-text {
  padding-top: 1rem;
  color: #dc3545;
  font-size: 0.9em;
  text-align: center;
}

.submit-section {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.ready-message {
  font-weight: bold;
  color: #28a745;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.action-buttons-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.button-base {
  padding: 0.75rem 1.5rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
  transition: background-color 0.2s ease;
}
.button-base:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.submit-button {
  padding: 0.75rem 1.5rem;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  text-transform: uppercase;
  transition: background-color 0.2s ease;
  background-color: #6790fc;
  border-radius: 4px;
}
.submit-button:hover:not(:disabled) {
  background-color: #5174cd;
}
.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.download-button {
  padding: 0.75rem 1.5rem;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  text-transform: uppercase;
  transition: background-color 0.2s ease;
  background-color: #28a745;
  text-decoration: none;
  border-radius: 4px;
}
.download-button:hover {
  background-color: #218838;
}
</style>
