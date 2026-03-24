<script setup>
import { computed } from 'vue'

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  apiBase: {
    type: String,
    required: true
  },
  compact: {
    type: Boolean,
    default: false
  }
})

const formattedHashtags = computed(() => {
  if (!props.post?.hashtags?.length) return ''
  return props.post.hashtags.map((tag) => (tag.startsWith('#') ? tag : `#${tag}`)).join(' ')
})

const imageSource = computed(() => {
  const image = props.post?.image_url
  if (!image) return ''
  if (image.startsWith('http://') || image.startsWith('https://')) return image
  return `${props.apiBase}/${image}`
})
</script>

<template>
  <article class="post-preview" :class="{ compact }">
    <div class="post-header">
      <div class="avatar">AI</div>
      <div>
        <h3>ai_post_simulator</h3>
        <small>{{ post.tone }} tone · {{ post.topic }}</small>
      </div>
    </div>

    <img v-if="imageSource" class="preview-image" :src="imageSource" alt="Generated post" />
    <div v-else class="image-placeholder">No image returned by the API.</div>

    <p class="caption">{{ post.caption }}</p>
    <p class="hashtags">{{ formattedHashtags }}</p>
  </article>
</template>

<style scoped>
.post-preview {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px;
  margin-top: 10px;
  background: #fff;
}

.compact {
  margin-top: 0;
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
</style>
