<script setup>
import { ref, watch, onMounted, computed } from 'vue'

const props = defineProps({
  kpi: { type: Object, required: true },
})

const display = ref(0)
const duration = 900

function formatNumber(n) {
  const isInt = Number.isInteger(props.kpi.value)
  const digits = isInt ? 0 : (props.kpi.value > 1000 ? 0 : 1)
  return n.toLocaleString('zh-CN', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
}

const formatted = computed(() => formatNumber(display.value))

function animate() {
  const start = performance.now()
  const from = 0
  const to = props.kpi.value
  function step(now) {
    const p = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - p, 3)
    display.value = from + (to - from) * eased
    if (p < 1) requestAnimationFrame(step)
    else display.value = to
  }
  requestAnimationFrame(step)
}

onMounted(animate)
watch(() => props.kpi.value, animate)

const iconColor = {
  'currency-yuan': '#FF8A65',
  'account-group': '#7CB342',
  cart: '#64B5F6',
  repeat: '#EC9BAE',
}
</script>

<template>
  <v-card class="kpi-card pa-5 h-100" flat>
    <div class="d-flex align-center justify-space-between">
      <div>
        <div class="kpi-label">{{ kpi.label }}</div>
        <div class="d-flex align-baseline mt-2">
          <span class="kpi-value font-num">{{ formatted }}</span>
          <span class="kpi-unit ml-1">{{ kpi.unit }}</span>
        </div>
        <div class="d-flex align-center mt-3">
          <v-icon
            :icon="kpi.trend >= 0 ? 'mdi-trending-up' : 'mdi-trending-down'"
            :color="kpi.trend >= 0 ? '#7CB342' : '#E57373'"
            size="16"
          />
          <span
            class="trend-val font-num ml-1"
            :style="{ color: kpi.trend >= 0 ? '#7CB342' : '#E57373' }"
          >
            {{ kpi.trend >= 0 ? '+' : '' }}{{ kpi.trend }}%
          </span>
          <span class="trend-label ml-2">同比</span>
        </div>
      </div>
      <div class="kpi-icon" :style="{ background: (iconColor[kpi.icon] || '#FF8A65') + '22' }">
        <v-icon :icon="'mdi-' + kpi.icon" :color="iconColor[kpi.icon] || '#FF8A65'" size="26" />
      </div>
    </div>
  </v-card>
</template>

<style scoped>
.kpi-card {
  background: linear-gradient(180deg, #ffffff 0%, #fffaf6 100%);
  border: 1px solid var(--c-line) !important;
  box-shadow: 0 12px 30px -20px rgba(166, 92, 62, 0.4) !important;
  transition: transform 0.25s ease;
}
.kpi-card:hover {
  transform: translateY(-4px);
}
.kpi-label {
  font-size: 0.9rem;
  color: var(--c-ink-soft);
  font-weight: 500;
}
.kpi-value {
  font-size: 2.1rem;
  font-weight: 700;
  color: var(--c-ink);
  line-height: 1;
}
.kpi-unit {
  font-size: 0.95rem;
  color: var(--c-ink-soft);
}
.trend-val {
  font-size: 0.85rem;
  font-weight: 600;
}
.trend-label {
  font-size: 0.78rem;
  color: #b39a8c;
}
.kpi-icon {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
