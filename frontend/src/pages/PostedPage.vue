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

    const found = data.posts.find((item) => item.id === route.params.id)
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

    <section v-else class="post-wrapper">
      <InstagramPostCard :post="post" :api-base="apiBase" compact />
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

.post-wrapper {
  max-width: 700px;
}

.error {
  background: #fee2e2;
  color: #b91c1c;
  border-radius: 8px;
  padding: 12px;
}
</style>
