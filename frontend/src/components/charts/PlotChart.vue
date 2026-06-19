<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Plotly from 'plotly.js-dist-min'
import { PLOT_CONFIG } from '../../constants/charts'

const props = defineProps({
  data: { type: Array, default: () => [] },
  layout: { type: Object, default: () => ({}) },
  config: { type: Object, default: () => ({}) },
  height: { type: String, default: '440px' },
})

const el = ref(null)

function render() {
  if (!el.value) return
  Plotly.react(el.value, props.data, props.layout, {
    ...PLOT_CONFIG,
    ...props.config,
  })
}

function resize() {
  if (el.value) Plotly.Plots.resize(el.value)
}

onMounted(() => {
  render()
  window.addEventListener('resize', resize)
})

watch(
  () => [props.data, props.layout],
  () => render(),
  { deep: true }
)

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  if (el.value) Plotly.purge(el.value)
})
</script>

<template>
  <div ref="el" class="plot-area" :style="{ height }"></div>
</template>

<style scoped>
.plot-area {
  width: 100%;
}
</style>
