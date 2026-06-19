<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import Plotly from 'plotly.js-dist-min'
import { PLOT_CONFIG } from '../../constants/charts'

const props = defineProps({
  data: { type: Array, default: () => [] },
  layout: { type: Object, default: () => ({}) },
  config: { type: Object, default: () => ({}) },
  height: { type: String, default: '440px' },
  chartTitle: { type: String, default: '' },
})

const el = ref(null)
const fullscreenEl = ref(null)
const dialog = ref(false)
const hovered = ref(false)

function render() {
  if (!el.value) return
  Plotly.react(el.value, props.data, props.layout, {
    ...PLOT_CONFIG,
    ...props.config,
  })
}

function renderFullscreen() {
  if (!fullscreenEl.value) return
  const bigLayout = {
    ...props.layout,
    margin: props.layout.margin
      ? { ...props.layout.margin, l: (props.layout.margin.l || 48) + 12, r: (props.layout.margin.r || 24) + 12 }
      : { l: 60, r: 36, t: 36, b: 60 },
    height: undefined,
  }
  Plotly.react(fullscreenEl.value, props.data, bigLayout, {
    ...PLOT_CONFIG,
    ...props.config,
    toImageButtonOptions: {
      ...(PLOT_CONFIG.toImageButtonOptions || {}),
      filename: props.chartTitle || 'baby-market-chart',
      height: 1000,
      width: 1600,
    },
  })
}

function resize() {
  if (el.value) Plotly.Plots.resize(el.value)
}

function resizeFullscreen() {
  if (fullscreenEl.value && dialog.value) Plotly.Plots.resize(fullscreenEl.value)
}

async function openFullscreen() {
  dialog.value = true
  await nextTick()
  setTimeout(() => renderFullscreen(), 80)
}

function closeFullscreen() {
  dialog.value = false
  setTimeout(() => {
    if (fullscreenEl.value) Plotly.purge(fullscreenEl.value)
  }, 200)
}

onMounted(() => {
  render()
  window.addEventListener('resize', resize)
  window.addEventListener('resize', resizeFullscreen)
})

watch(
  () => [props.data, props.layout],
  () => {
    render()
    if (dialog.value) renderFullscreen()
  },
  { deep: true }
)

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  window.removeEventListener('resize', resizeFullscreen)
  if (el.value) Plotly.purge(el.value)
  if (fullscreenEl.value) Plotly.purge(fullscreenEl.value)
})
</script>

<template>
  <div
    class="plot-wrapper"
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
  >
    <div ref="el" class="plot-area" :style="{ height }"></div>
    <v-btn
      class="fullscreen-btn"
      variant="flat"
      color="primary"
      size="small"
      density="compact"
      @click="openFullscreen"
      :class="{ 'show': hovered }"
    >
      <v-icon start icon="mdi-fullscreen" size="16" />全屏
    </v-btn>

    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      content-class="dialog-content-holder"
      transition="dialog-fade-transition"
    >
      <div class="fs-mask" @click.self="closeFullscreen"></div>
      <div class="fs-card" @click.stop>
        <div class="fs-header">
          <div class="fs-title">
            <v-icon icon="mdi-chart-line" size="20" color="#FF8A65" />
            <span>{{ chartTitle || '图表全屏查看' }}</span>
          </div>
          <v-btn
            variant="text"
            size="small"
            icon="mdi-close"
            @click="closeFullscreen"
            class="close-btn"
          >
            <v-icon icon="mdi-close" size="22" />
          </v-btn>
        </div>
        <div ref="fullscreenEl" class="fs-plot"></div>
      </div>
    </v-dialog>
  </div>
</template>

<style scoped>
.plot-wrapper {
  position: relative;
  width: 100%;
}
.plot-area {
  width: 100%;
}
.fullscreen-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transform: translateY(-4px);
  transition: opacity 0.2s ease, transform 0.2s ease;
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(4px);
  box-shadow: 0 4px 14px -6px rgba(255, 138, 101, 0.45);
  z-index: 3;
  color: #e5704f !important;
  font-weight: 600;
  font-size: 0.8rem;
}
.fullscreen-btn.show {
  opacity: 1;
  transform: translateY(0);
}

.dialog-content-holder {
  background: transparent !important;
  padding: 0 !important;
}

.fs-mask {
  position: fixed;
  inset: 0;
  background: rgba(78, 52, 46, 0.55);
  backdrop-filter: blur(6px);
  z-index: 1;
}

.fs-card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: calc(100% - 80px);
  max-width: 1600px;
  height: calc(100% - 80px);
  max-height: 900px;
  background: linear-gradient(180deg, #ffffff 0%, #fffaf6 100%);
  border-radius: 20px;
  box-shadow: 0 32px 80px -20px rgba(78, 52, 46, 0.4);
  z-index: 2;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: pop-in 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes pop-in {
  from {
    opacity: 0;
    transform: translate(-50%, -48%) scale(0.94);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

.fs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px 14px 24px;
  border-bottom: 1px solid #f0ddd2;
  background: #fff8f3;
}

.fs-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-serif);
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--c-ink);
}

.close-btn {
  color: #a1887f !important;
  width: 38px;
  height: 38px;
  border-radius: 12px;
  transition: all 0.2s;
}
.close-btn:hover {
  background: #ffe7da !important;
  color: #e5704f !important;
}

.fs-plot {
  flex: 1;
  width: 100%;
  min-height: 0;
}

@media (max-width: 768px) {
  .fs-card {
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    border-radius: 0;
  }
}
</style>
