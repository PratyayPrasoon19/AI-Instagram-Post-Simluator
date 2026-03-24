<script setup>
import { computed, onMounted, ref } from 'vue'

const topic = ref('')
const tone = ref('professional')
const loading = ref(false)
const posting = ref(false)
const error = ref('')
const successMessage = ref('')
const generatedPost = ref(null)
const history = ref([])
const historyLoading = ref(false)

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const hashtagsText = computed(() => {
  if (!generatedPost.value?.hashtags?.length) return ''
  return generatedPost.value.hashtags.map((tag) => (tag.startsWith('#') ? tag : `#${tag}`)).join(' ')
})

async function fetchHistory() {
  historyLoading.value = true
  try {
    const response = await fetch(`${apiBase}/history`)
    const data = await response.json()

    if (data.status === 'success') {
      history.value = data.posts
    } else {
      error.value = data.message || 'Failed to load history.'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    historyLoading.value = false
  }
}

async function generatePost() {
  error.value = ''
  successMessage.value = ''

  if (!topic.value.trim()) {
    error.value = 'Please enter a topic.'
    return
  }

  loading.value = true
  try {
    const response = await fetch(`${apiBase}/generate-post`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        topic: topic.value,
        tone: tone.value
      })
    })

    const data = await response.json()

    if (data.status === 'success') {
      generatedPost.value = data
      await fetchHistory()
    } else {
      error.value = data.message || 'Failed to generate post.'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function simulatePost() {
  if (!generatedPost.value?.post_id) return

  posting.value = true
  error.value = ''
  successMessage.value = ''

  try {
    const response = await fetch(`${apiBase}/post/${generatedPost.value.post_id}`, {
      method: 'POST'
    })
    const data = await response.json()

    if (data.status === 'success') {
      successMessage.value = data.message
      await fetchHistory()
    } else {
      error.value = data.message || 'Failed to post on Instagram (simulation).'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    posting.value = false
  }
}

onMounted(fetchHistory)
</script>

<template>
  <div class="layout">
    <header>
      <h1>AI Instagram Post Generator</h1>
      <p>Generate captions, hashtags, and images, then simulate posting to Instagram.</p>
    </header>

    <section class="card form-card">
      <h2>Generate Post</h2>
      <div class="input-group">
        <label for="topic">Topic</label>
        <input id="topic" v-model="topic" type="text" placeholder="e.g. Productivity tips for students" />
      </div>

      <div class="input-group">
        <label for="tone">Tone</label>
        <select id="tone" v-model="tone">
          <option value="professional">Professional</option>
          <option value="casual">Casual</option>
        </select>
      </div>

      <button class="primary" :disabled="loading" @click="generatePost">
        {{ loading ? 'Generating...' : 'Generate Post' }}
      </button>
    </section>

    <p v-if="error" class="alert error">{{ error }}</p>
    <p v-if="successMessage" class="alert success">{{ successMessage }}</p>

    <section v-if="generatedPost" class="card preview-card">
      <h2>Instagram Post Preview</h2>
      <div class="post-preview">
        <div class="post-header">
          <div class="avatar">AI</div>
          <div>
            <h3>ai_post_simulator</h3>
            <small>{{ generatedPost.tone }} tone · {{ generatedPost.topic }}</small>
          </div>
        </div>

        <img
          v-if="generatedPost.image_url"
          class="preview-image"
          :src="`${apiBase}/${generatedPost.image_url}`"
          alt="Generated post"
        />
        <div v-else class="image-placeholder">No image returned by the API.</div>

        <p class="caption">{{ generatedPost.caption }}</p>
        <p class="hashtags">{{ hashtagsText }}</p>
      </div>

      <button class="secondary" :disabled="posting" @click="simulatePost">
        {{ posting ? 'Posting...' : 'Simulate Post (/post endpoint)' }}
      </button>
    </section>

    <section class="card history-card">
      <div class="history-title">
        <h2>Generated Post History</h2>
        <button class="ghost" :disabled="historyLoading" @click="fetchHistory">
          {{ historyLoading ? 'Refreshing...' : 'Refresh' }}
        </button>
      </div>

      <p v-if="!history.length" class="empty">No posts yet.</p>
      <ul v-else class="history-list">
        <li v-for="item in history" :key="item.id" class="history-item">
          <div>
            <h3>{{ item.topic }}</h3>
            <small>{{ item.tone }} · {{ new Date(item.created_at).toLocaleString() }}</small>
          </div>
          <span :class="item.posted ? 'posted-badge' : 'draft-badge'">
            {{ item.posted ? 'Posted' : 'Draft' }}
          </span>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  gap: 20px;
}

header h1 {
  font-size: 30px;
}

header p {
  color: #6b7280;
  margin-top: 4px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.08);
}

.form-card {
  display: grid;
  gap: 12px;
}

.input-group {
  display: grid;
  gap: 6px;
}

input,
select {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 10px;
}

.primary {
  background: #2563eb;
  color: white;
}

.secondary {
  background: #111827;
  color: white;
  margin-top: 12px;
}

.ghost {
  background: #f3f4f6;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.post-preview {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px;
  margin-top: 10px;
}

.post-header {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 12px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #111827;
  color: white;
  display: grid;
  place-items: center;
  font-size: 13px;
}

.preview-image {
  width: 100%;
  border-radius: 10px;
  margin-bottom: 10px;
  max-height: 500px;
  object-fit: cover;
}

.image-placeholder {
  padding: 40px;
  text-align: center;
  border: 1px dashed #9ca3af;
  border-radius: 8px;
  color: #6b7280;
  margin-bottom: 10px;
}

.caption {
  margin-top: 8px;
  white-space: pre-wrap;
}

.hashtags {
  color: #2563eb;
  margin-top: 8px;
}

.alert {
  border-radius: 8px;
  padding: 12px;
}

.error {
  background: #fee2e2;
  color: #b91c1c;
}

.success {
  background: #dcfce7;
  color: #166534;
}

.history-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-list {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
  display: grid;
  gap: 10px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px;
}

.posted-badge,
.draft-badge {
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
}

.posted-badge {
  background: #dcfce7;
  color: #166534;
}

.draft-badge {
  background: #f3f4f6;
  color: #374151;
}

.empty {
  color: #6b7280;
  margin-top: 10px;
}
</style>
