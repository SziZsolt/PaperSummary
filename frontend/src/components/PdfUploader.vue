<template>
  <form @submit.prevent="submit" class="uploader">
    <label>
      Domain:
      <select v-model="domain" required>
        <option disabled value="">-- select domain --</option>
        <option value="machine-learning">Machine Learning</option>
        <option value="computer-science">Computer Science</option>
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
    }
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
        // TODO: Delete
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))
        await delay(5000)
        // TODO: Replace the following mock response with an actual API call to your backend
        const resp = {
            method: 'POST',
            body: form,
            ok: true,
            json: async () => ({ summary: `Mock summary for domain "${this.domain}" and file "${this.file.name}"` }),
        }

        if (!resp.ok) throw new Error(`Server error: ${resp.statusText}`)

        const data = await resp.json()
        const summary = data.summary || JSON.stringify(data, null, 2)
        this.$emit('summary', { loading: false, summary, error: null })
      } catch (err) {
        this.$emit('summary', { loading: false, summary: null, error: err.message })
      } finally {
        this.loading = false
      }
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
</style>
