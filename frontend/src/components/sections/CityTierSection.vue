<script setup>
import { computed } from 'vue'
import PlotChart from '../charts/PlotChart.vue'
import { COLOR, plotLayout } from '../../constants/charts'
import { useDashboardStore } from '../../stores/dashboard'

const props = defineProps({
  data: { type: Object, default: null },
})

const emit = defineEmits(['data-click'])

const store = useDashboardStore()

const heatTrace = computed(() => {
  const d = props.data
  if (!d) return []
  const cats = d.preference.map((r) => r.category)
  const z = d.preference.map((r) => d.tiers.map((t) => r[t]))
  const filtered = store.sharedFilter.value
  const opacity = cats.map((cat) =>
    filtered ? (store.isFilteredCategory(cat) ? 1 : 0.35) : 1
  )
  return [
    {
      z,
      x: d.tiers,
      y: cats,
      type: 'heatmap',
      colorscale: [
        [0, '#FFF3EC'],
        [0.35, '#FFD0B8'],
        [0.7, '#FF9F7E'],
        [1, '#E55A2B'],
      ],
      hovertemplate: '<b>%{y}</b><br>%{x}: %{z:.0f} 元/人<extra></extra>',
      showscale: true,
      colorbar: {
        title: { text: '元/人', font: { size: 10, color: '#6d5546' } },
        tickfont: { size: 9, color: '#a1887f' },
        len: 0.85,
      },
      text: z.map((row, i) => row.map((v) => v.toFixed(0))),
      texttemplate: '%{text}',
      textfont: z.map((row, i) =>
        row.map(() => ({
          size: 11,
          color: filtered
            ? (store.isFilteredCategory(cats[i]) ? '#4e342e' : '#8d6e63')
            : '#4e342e',
        }))
      ),
      opacity,
    },
  ]
})

const heatLayout = computed(() => {
  const d = props.data
  if (!d) return plotLayout({})
  const cats = d.preference.map((r) => r.category)
  const filtered = store.sharedFilter.value
  const shapes = []
  if (filtered) {
    const matchIdx = cats.findIndex((c) => store.isFilteredCategory(c))
    if (matchIdx >= 0) {
      const n = cats.length
      const y0 = matchIdx - 0.5
      const y1 = matchIdx + 0.5
      shapes.push({
        type: 'rect',
        x0: -0.5,
        y0,
        x1: d.tiers.length - 0.5,
        y1,
        line: {
          color: '#E5704F',
          width: 2.5,
        },
        fillcolor: 'rgba(255, 193, 160, 0.25)',
        layer: 'below',
      })
    }
  }
  return plotLayout({
    height: 460,
    margin: { l: 110, r: 24, t: 16, b: 40 },
    yaxis: {
      automargin: true,
      tickfont: cats.map((cat) => ({
        size: filtered
          ? (store.isFilteredCategory(cat) ? 13 : 10)
          : 11,
        color: filtered
          ? (store.isFilteredCategory(cat) ? '#E5704F' : '#8d6e63')
          : '#6d5546',
        weight: filtered
          ? (store.isFilteredCategory(cat) ? 'bold' : 'normal')
          : 'normal',
      })),
    },
    xaxis: { tickfont: { size: 12, color: '#6d5546' } },
    shapes,
  })
})

const tierColor = { 一线城市: COLOR.coral, 二线城市: COLOR.mint, 下沉市场: COLOR.sky }

const boxTraces = computed(() => {
  const d = props.data
  if (!d) return []
  const filtered = store.sharedFilter.value
  const traces = []
  for (const tier of d.tiers) {
    const arr = d.price_distribution[tier]
    if (!arr) continue
    const catNames = arr.map((r) => r.category)
    const lineWidths = catNames.map((c) =>
      filtered ? (store.isFilteredCategory(c) ? 3 : 1.2) : 2
    )
    const opacities = catNames.map((c) =>
      filtered ? (store.isFilteredCategory(c) ? 1 : 0.35) : 1
    )
    traces.push({
      type: 'box',
      x: catNames,
      q1: arr.map((r) => r.q1),
      median: arr.map((r) => r.median),
      q3: arr.map((r) => r.q3),
      lowerfence: arr.map((r) => r.min),
      upperfence: arr.map((r) => r.max),
      name: tier,
      marker: { color: tierColor[tier], opacity: opacities },
      line: {
        color: tierColor[tier],
        width: lineWidths,
      },
      fillcolor: tierColor[tier] + '33',
      boxpoints: false,
      offsetgroup: tier,
      opacity: filtered ? 0.9 : 1,
    })
  }
  return traces
})

const boxLayout = computed(() => {
  const d = props.data
  const filtered = store.sharedFilter.value
  return plotLayout({
    height: 380,
    margin: { l: 56, r: 24, t: 16, b: 90 },
    boxmode: 'group',
    xaxis: {
      tickangle: -35,
      gridcolor: '#F0DDD2',
      tickfont: d?.price_distribution?.['一线城市']?.map?.((r) => ({
        size: filtered
          ? (store.isFilteredCategory(r.category) ? 12 : 10)
          : 10,
        color: filtered
          ? (store.isFilteredCategory(r.category) ? '#E5704F' : '#8d6e63')
          : '#6d5546',
        weight: filtered
          ? (store.isFilteredCategory(r.category) ? 'bold' : 'normal')
          : 'normal',
      })),
    },
    yaxis: { title: '价格（元）', gridcolor: '#F0DDD2' },
    legend: { orientation: 'h', y: -0.42, font: { size: 11 } },
  })
})

function onDataClick(payload) {
  emit('data-click', payload)
}
</script>

<template>
  <div v-if="data">
    <v-row>
      <v-col cols="12" md="6">
        <div class="chart-hint mb-1">品类偏好热力图 · 人均消费（元/人）</div>
        <PlotChart
          :data="heatTrace"
          :layout="heatLayout"
          :chart-title="'各城市层级品类偏好热力图'"
          height="460px"
          :clickable="true"
          @data-click="onDataClick"
        />
      </v-col>
      <v-col cols="12" md="6">
        <div class="chart-hint mb-1">价格带分布箱线图 · 一线 / 二线 / 下沉市场</div>
        <PlotChart
          :data="boxTraces"
          :layout="boxLayout"
          :chart-title="'各城市层级品类价格带分布箱线图'"
          height="380px"
          :clickable="true"
          @data-click="onDataClick"
        />
      </v-col>
    </v-row>
  </div>
  <v-skeleton-loader v-else type="image" height="420" />
</template>

<style scoped>
.chart-hint {
  font-size: 0.82rem;
  color: var(--c-ink-soft);
  font-weight: 500;
}
</style>
