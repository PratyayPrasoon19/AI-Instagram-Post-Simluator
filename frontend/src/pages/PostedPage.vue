<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import InstagramPostCard from '../components/InstagramPostCard.vue'

const route = useRoute()
const router = useRouter()

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const loading = ref(true)
const error = ref('')
const post = ref(null)

async function loadPostedPost() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(`${apiBase}/history`)
    const data = await response.json()

    if (data.status !== 'success') {
      error.value = data.message || 'Unable to fetch post.'
      return
    }

    const found = data.posts.find((item) => String(item.id) === String(route.params.id))
    if (!found) {
      error.value = 'Post not found in history.'
      return
    }

    post.value = found
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(loadPostedPost)
</script>

<template>
  <div class="posted-page">
    <div class="top-row">
      <h1>Posted on Instagram (Simulation)</h1>
      <button class="back" @click="router.push('/')">Back to Generator</button>
    </div>

    <p v-if="loading">Loading post...</p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <section v-else class="instagram-shell">
      <div class="instagram-header">
        <strong>Instagram</strong>
        <span>Just now</span>
      </div>
      <InstagramPostCard :post="post" :api-base="apiBase" compact />
      <div class="instagram-footer">
        <span>❤️ 128 likes</span>
        <span>💬 14 comments</span>
        <span>📤 Share</span>
      </div>
    </section>
  </div>
</template>

<style scoped>
.posted-page {
  display: grid;
  gap: 14px;
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  margin: 0;
  font-size: 28px;
}

.back {
  background: #111827;
  color: white;
}

.instagram-shell {
  max-width: 520px;
  background: #fff;
  border: 1px solid #dbdbdb;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.08);
}

.instagram-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #efefef;
}

.instagram-header span {
  color: #6b7280;
  font-size: 13px;
}

.instagram-footer {
  display: flex;
  gap: 16px;
  padding: 10px 16px 14px;
  color: #1f2937;
  font-size: 14px;
  border-top: 1px solid #efefef;
}

.error {
  background: #fee2e2;
  color: #b91c1c;
  border-radius: 8px;
  padding: 12px;
}
</style>
