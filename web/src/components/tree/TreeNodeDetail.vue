<script setup>
import { ref, watch, computed } from 'vue'
import MarkdownIt from 'markdown-it'
import { getNode } from '@/api/documents'

const props = defineProps({
  documentId: { type: String, required: true },
  nodeId: { type: String, required: true },
})

const emit = defineEmits(['close'])

const nodeDetail = ref(null)
const loading = ref(false)

const md = new MarkdownIt({ html: false, linkify: true })

// Does the node text contain Markdown image references? If so we render it
// as Markdown so extracted images display inline; otherwise keep the plain
// monospace <pre> view.
const hasImages = computed(() => {
  const t = nodeDetail.value?.text
  return !!t && /!\[[^\]]*\]\([^)]+\)/.test(t)
})

const renderedText = computed(() => {
  if (!nodeDetail.value?.text) return ''
  return md.render(nodeDetail.value.text)
})

watch(() => props.nodeId, async (id) => {
  if (!id) return
  loading.value = true
  try {
    nodeDetail.value = await getNode(props.documentId, id)
  } catch (e) {
    nodeDetail.value = null
  } finally {
    loading.value = false
  }
}, { immediate: true })
</script>

<template>
  <div class="node-detail">
    <div class="node-detail__header">
      <h3 class="node-detail__title">Node Detail</h3>
      <button class="node-detail__close" @click="emit('close')">✕</button>
    </div>

    <div v-if="loading" class="node-detail__loading">Loading...</div>

    <div v-else-if="nodeDetail" class="node-detail__body">
      <div class="node-detail__field">
        <label>Title</label>
        <p>{{ nodeDetail.title }}</p>
      </div>

      <div class="node-detail__row">
        <div class="node-detail__field" v-if="nodeDetail.node_id">
          <label>Node ID</label>
          <code>{{ nodeDetail.node_id }}</code>
        </div>
        <div class="node-detail__field" v-if="nodeDetail.start_index">
          <label>Pages</label>
          <p>{{ nodeDetail.start_index }} - {{ nodeDetail.end_index }}</p>
        </div>
      </div>

      <div class="node-detail__field" v-if="nodeDetail.summary">
        <label>Summary</label>
        <p class="node-detail__text">{{ nodeDetail.summary }}</p>
      </div>

      <div class="node-detail__field" v-if="nodeDetail.text">
        <label>Full Text</label>
        <div
          v-if="hasImages"
          class="node-detail__text node-detail__text--md markdown-body"
          v-html="renderedText"
        ></div>
        <pre v-else class="node-detail__text node-detail__text--pre">{{ nodeDetail.text }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.node-detail {
  width: 320px;
  border-left: 1px solid var(--color-border);
  background: var(--color-bg-primary);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.node-detail__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-border);
}

.node-detail__title {
  font-size: var(--text-sm);
  font-weight: 600;
}

.node-detail__close {
  color: var(--color-text-muted);
  font-size: var(--text-sm);
  padding: 4px;
}

.node-detail__close:hover {
  color: var(--color-text-primary);
}

.node-detail__loading {
  padding: var(--space-lg);
  text-align: center;
  color: var(--color-text-muted);
}

.node-detail__body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.node-detail__row {
  display: flex;
  gap: var(--space-md);
}

.node-detail__field label {
  display: block;
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.node-detail__field p, .node-detail__field code {
  font-size: var(--text-sm);
  line-height: 1.5;
}

.node-detail__field code {
  font-family: var(--font-mono);
  background: var(--color-bg-tertiary);
  padding: 2px 6px;
  border-radius: 4px;
}

.node-detail__text {
  max-height: 300px;
  overflow-y: auto;
  font-size: var(--text-sm);
  line-height: 1.6;
  color: var(--color-text-secondary);
}

.node-detail__text--pre {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  white-space: pre-wrap;
  word-break: break-word;
  background: var(--color-bg-tertiary);
  padding: var(--space-sm);
  border-radius: var(--border-radius);
}

.node-detail__text--md :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: var(--border-radius);
  margin: var(--space-sm) 0;
  display: block;
}

.node-detail__text--md :deep(p) {
  margin: var(--space-xs) 0;
}
</style>
