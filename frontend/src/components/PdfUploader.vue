<template>
  <form @submit.prevent="submit" class="uploader">
    <label>
      Domain:
      <div v-if="domainsLoading" class="domain-loader">
        <span class="spinner" aria-hidden="true"></span>
        <span>Loading domains…</span>
      </div>
      <select v-else v-model="domain" required>
        <option disabled value="">-- select domain --</option>
        <option v-for="d in domains" :key="d.id" :value="d.id">{{ d.label }}</option>
      </select>
    </label>

    <label>
      PDF file:
      <input ref="fileInput" type="file" accept="application/pdf" @change="onFileChange" required />
    </label>

    <button type="submit" :disabled="loading">
      <template v-if="loading">
        <span class="spinner" aria-hidden="true"></span>
        <span style="margin-left:8px">Processing…</span>
      </template>
      <template v-else>Upload &amp; Summarize</template>
    </button>

    <div v-if="domainsError" class="error">Could not load domains: {{ domainsError }}</div>
  </form>
</template>

<script>
export default {
  name: 'PdfUploader',
  data() {
    return {
      domain: '',
      file: null,
      loading: false,
      domains: [],
      domainsError: null,
      domainsLoading: false,
    }
  },
  mounted() {
    // Load domains via an async provider function. Currently the provider
    // returns a mocked list (so the UI behaves like it's async without
    // calling the backend). Later we can replace fetchDomains with a real
    // fetch to the backend (/domains).
    this.domainsLoading = true
    this.fetchDomains()
      .then((list) => {
        this.domains = list
        if (this.domains.length > 0) this.domain = this.domains[0].id
      })
      .catch((err) => {
        this.domainsError = err.message || String(err)
      })
      .finally(() => {
        this.domainsLoading = false
      })
  },
  methods: {
    onFileChange(e) {
      const f = e.target.files && e.target.files[0]
      this.file = f || null
    },
    async submit() {
      if (!this.file || !this.domain) return
      this.loading = true
      this.$emit('summary', { loading: true, summary: null, error: null })

      try {
        const form = new FormData()
        form.append('domain', this.domain)
        form.append('file', this.file)

        // simulate network / processing delay with a mock response
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))
        await delay(1500)

        const data = { summary: `Mock summary for domain \"${this.domain}\" and file \"${this.file.name}\"` }
        const summary = data.summary || JSON.stringify(data, null, 2)
        this.$emit('summary', { loading: false, summary, error: null })
      } catch (err) {
        this.$emit('summary', { loading: false, summary: null, error: err.message })
      } finally {
        this.loading = false
      }
    },
    // Async provider for domains. Right now it returns a mocked list after
    // a tiny delay to simulate network latency. Replace implementation to
    // call the real backend endpoint when ready.
    async fetchDomains() {
      // Simulate a short network delay so the loading state is visible.
      await new Promise((r) => setTimeout(r, 1500))
      return [
        { id: 'computer-science', label: 'Computer Science' },
        { id: 'machine-learning', label: 'Machine Learning' },
      ]
    },
  },
}
</script>

<style scoped>
.uploader {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

input[type="text"], input[type="file"] {
  display: block;
  margin-top: 6px;
}

button {
  width: max-content;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
}

button:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(0,0,0,0.15);
  border-top-color: rgba(0,0,0,0.6);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.domain-loader {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: 6px;
}
</style>
