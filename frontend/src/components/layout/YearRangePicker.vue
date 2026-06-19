<script setup>
import { ref, computed, watch } from 'vue'
import { useDashboardStore, MIN_YEAR, MAX_YEAR } from '../../stores/dashboard'

const emit = defineEmits(['change'])

const store = useDashboardStore()

const startYear = ref(store.yearRange.start)
const endYear = ref(store.yearRange.end)
const showDropdown = ref(false)

const rangeValue = computed({
  get: () => [startYear.value, endYear.value],
  set: (val) => {
    startYear.value = val[0]
    endYear.value = val[1]
  },
})

const years = computed(() => {
  const arr = []
  for (let y = MIN_YEAR; y <= MAX_YEAR; y++) {
    arr.push(y)
  }
  return arr
})

const rangeLabel = computed(() => {
  if (store.drillDownYear) {
    return `${store.drillDownYear} 年（下钻）`
  }
  if (startYear.value === endYear.value) {
    return `${startYear.value} 年`
  }
  return `${startYear.value} - ${endYear.value} 年`
})

const quickRanges = [
  { label: '全部', start: MIN_YEAR, end: MAX_YEAR },
  { label: '近5年', start: MAX_YEAR - 4, end: MAX_YEAR },
  { label: '近3年', start: MAX_YEAR - 2, end: MAX_YEAR },
  { label: '2020-2024', start: 2020, end: 2024 },
  { label: '2010-2015', start: 2010, end: 2015 },
]

function validateRange() {
  if (startYear.value > endYear.value) {
    const temp = startYear.value
    startYear.value = endYear.value
    endYear.value = temp
  }
}

async function applyRange() {
  validateRange()
  showDropdown.value = false
  await store.setYearRange(startYear.value, endYear.value)
  emit('change', { start: startYear.value, end: endYear.value })
}

async function applyQuickRange(range) {
  startYear.value = range.start
  endYear.value = range.end
  showDropdown.value = false
  await store.setYearRange(range.start, range.end)
  emit('change', { start: range.start, end: range.end })
}

async function selectSingleYear(year) {
  startYear.value = year
  endYear.value = year
  showDropdown.value = false
  await store.setYearRange(year, year)
  emit('change', { start: year, end: year })
}

function toggleDropdown() {
  if (store.loading) return
  showDropdown.value = !showDropdown.value
}

function closeDropdown(e) {
  if (!e.target.closest('.year-range-wrapper')) {
    showDropdown.value = false
  }
}

watch(
  () => [store.yearRange.start, store.yearRange.end],
  ([s, e]) => {
    startYear.value = s
    endYear.value = e
  }
)

if (typeof window !== 'undefined') {
  window.addEventListener('click', closeDropdown)
}
</script>

<template>
  <div class="year-range-wrapper">
    <v-btn
      variant="flat"
      color="primary"
      size="small"
      density="comfortable"
      class="range-trigger"
      :disabled="store.loading"
      @click="toggleDropdown"
    >
      <v-icon icon="mdi-calendar-range" size="16" />
      <span class="range-label">{{ rangeLabel }}</span>
      <v-icon icon="mdi-chevron-down" size="16" :class="{ 'rotated': showDropdown }" />
    </v-btn>

    <transition
      enter-active-class="dropdown-enter"
      leave-active-class="dropdown-leave"
    >
      <div v-if="showDropdown" class="dropdown-panel">
        <div class="panel-header">
          <span class="panel-title">选择时间范围</span>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="x-small"
            @click="showDropdown = false"
          />
        </div>

        <div class="quick-ranges">
          <div class="section-label">快捷选择</div>
          <div class="quick-buttons">
            <v-btn
              v-for="r in quickRanges"
              :key="r.label"
              variant="tonal"
              size="x-small"
              density="compact"
              :color="startYear === r.start && endYear === r.end ? 'primary' : ''"
              @click="applyQuickRange(r)"
            >
              {{ r.label }}
            </v-btn>
          </div>
        </div>

        <div class="range-slider-section">
          <div class="section-label">范围滑块</div>
          <div class="slider-row">
            <div class="year-display start">
              <v-select
                v-model="startYear"
                :items="years"
                density="compact"
                variant="outlined"
                hide-details
                class="year-select"
                :menu-props="{ contentClass: 'year-dropdown-menu' }"
              />
            </div>
            <v-divider class="range-divider" />
            <div class="year-display end">
              <v-select
                v-model="endYear"
                :items="years"
                density="compact"
                variant="outlined"
                hide-details
                class="year-select"
                :menu-props="{ contentClass: 'year-dropdown-menu' }"
              />
            </div>
          </div>
          <v-range-slider
            v-model="rangeValue"
            :min="MIN_YEAR"
            :max="MAX_YEAR"
            :step="1"
            :tick-labels="years"
            ticks="always"
            show-ticks
            color="primary"
            thumb-label="always"
            class="range-slider"
          />
        </div>

        <div class="single-year-section">
          <div class="section-label">单年份选择（点击直接应用）</div>
          <div class="year-chips">
            <v-chip
              v-for="y in years"
              :key="y"
              size="small"
              :color="startYear === y && endYear === y ? 'primary' : ''"
              :variant="startYear === y && endYear === y ? 'flat' : 'tonal'"
              @click="selectSingleYear(y)"
              class="year-chip"
            >
              {{ y }}
            </v-chip>
          </div>
        </div>

        <div class="panel-actions">
          <v-btn
            variant="tonal"
            size="small"
            @click="showDropdown = false"
          >
            取消
          </v-btn>
          <v-btn
            variant="flat"
            color="primary"
            size="small"
            :loading="store.loading"
            @click="applyRange"
          >
            应用筛选
          </v-btn>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.year-range-wrapper {
  position: relative;
  display: inline-block;
}

.range-trigger {
  gap: 6px;
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid var(--c-line);
  border-radius: 10px !important;
  padding: 0 14px !important;
  min-width: 160px;
  transition: all 0.2s ease;
}

.range-trigger:hover:not(:disabled) {
  background: #fff !important;
  box-shadow: 0 4px 12px -6px rgba(255, 138, 101, 0.4);
}

.range-trigger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.range-label {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--c-ink);
}

.rotated {
  transform: rotate(180deg);
  transition: transform 0.2s ease;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 420px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 16px 48px -12px rgba(78, 52, 46, 0.25);
  border: 1px solid var(--c-line);
  z-index: 100;
  padding: 16px;
  animation: dropdown-in 0.2s ease;
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--c-line);
}

.panel-title {
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--c-ink);
  font-family: var(--font-serif);
}

.section-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #8d6e63;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.quick-ranges {
  margin-bottom: 16px;
}

.quick-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.range-slider-section {
  margin-bottom: 16px;
}

.slider-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.year-display {
  flex: 1;
}

.range-divider {
  flex-shrink: 0;
  width: 20px;
  border-color: #d7ccc8;
}

.year-select {
  width: 100%;
}

.year-select :deep(.v-field__input) {
  padding: 6px 10px !important;
  font-size: 0.85rem;
  font-weight: 600;
}

.range-slider {
  padding: 8px 4px 0;
}

.range-slider :deep(.v-slider-track__tick-label) {
  font-size: 0.7rem;
  color: #8d6e63;
}

.single-year-section {
  margin-bottom: 16px;
}

.year-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.year-chip {
  cursor: pointer;
  transition: all 0.15s ease;
}

.year-chip:hover {
  transform: translateY(-1px);
}

.panel-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid var(--c-line);
}

.year-dropdown-menu {
  max-height: 300px !important;
}

@media (max-width: 768px) {
  .dropdown-panel {
    min-width: calc(100vw - 32px);
    right: auto;
    left: 50%;
    transform: translateX(-50%);
  }

  .range-label {
    font-size: 0.8rem;
  }

  .range-trigger {
    min-width: auto;
    padding: 0 10px !important;
  }
}
</style>
