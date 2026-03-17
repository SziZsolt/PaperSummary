<template>
  <div class="container">
    <h1>Scientific Paper Summarizer</h1>
    <PdfUploader @summary="onSummary" />

    <section class="result" v-if="summary || loading || error">
      <h2>Summary</h2>
      <div v-if="loading" class="loading-block">
        <div class="spinner spinner-large" role="status" aria-label="Loading"></div>
        <div class="spinner-label">Loading summary…</div>
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <pre v-if="summary">{{ summary }}</pre>
    </section>
  </div>
</template>

<script>
import PdfUploader from './components/PdfUploader.vue'

export default {
  name: 'App',
  components: { PdfUploader },
  data() {
    return {
      summary: null,
      loading: false,
      error: null,
    }
  },
  methods: {
    onSummary(payload) {
      this.summary = payload.summary
      this.loading = payload.loading
      this.error = payload.error
    },
  },
}
</script>

<style>
.container {
  max-width: 760px;
  margin: 40px auto;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  padding: 0 16px;
}

.result pre {
  background: #f7f7f8;
  padding: 12px;
  border-radius: 6px;
  white-space: pre-wrap;
}

.error { color: #a33; }
</style>
