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

const trendTraces = computed(() => {
  const d = props.data
  if (!d) return []
  const years = d.market_size.map((r) => r.year)
  const traces = [
    {
      type: 'bar',
      x: years,
      y: d.market_size.map((r) => r.market_size),
      name: '市场规模（元）',
      yaxis: 'y2',
      marker: { color: '#FFD9C9', line: { color: '#FFCBB3', width: 1 } },
      hovertemplate: '<b>%{x}年</b><br>市场规模 %{y:,.0f} 元<extra></extra>',
    },
    {
      type: 'scatter',
      mode: 'lines+markers',
      x: d.birth_trend.map((r) => r.year),
      y: d.birth_trend.map((r) => r.birth_count),
      name: '出生人口（万）',
      yaxis: 'y',
      line: { color: COLOR.coral, width: 3, shape: 'spline' },
      marker: {
        size: 8,
        color: d.birth_trend.map((r) => (r.special_tag ? COLOR.rose : COLOR.coral)),
        line: { color: '#fff', width: 2 },
      },
      hovertemplate: '<b>%{x}年</b><br>出生 %{y} 万<extra></extra>',
    },
  ]
  return traces
})

const trendLayout = computed(() => {
  const d = props.data
  if (!d) return {}
  const shapes = d.special_years.map((sy) => ({
    type: 'rect',
    xref: 'x',
    yref: 'paper',
    x0: sy.year - 0.4,
    x1: sy.year + 0.4,
    y0: 0,
    y1: 1,
    fillcolor: COLOR.rose + '1a',
    line: { width: 0 },
  }))
  return plotLayout({
    height: 380,
    margin: { l: 52, r: 60, t: 16, b: 40 },
    xaxis: { gridcolor: '#F0DDD2' },
    yaxis: { title: '出生人口（万）', gridcolor: '#F0DDD2', side: 'left' },
    yaxis2: {
      title: '市场规模（元）',
      overlaying: 'y',
      side: 'right',
      gridcolor: 'rgba(0,0,0,0)',
      tickfont: { color: '#b39a8c' },
    },
    legend: { orientation: 'h', y: 1.12, x: 0.2, font: { size: 11 } },
    shapes,
    annotations: d.special_years.map((sy) => ({
      x: sy.year,
      y: 1,
      yref: 'paper',
      text: sy.tag.replace('年份', '').replace('期间', ''),
      showarrow: false,
      font: { size: 9, color: COLOR.rose },
      yshift: 8,
    })),
  })
})

const impactTrace = computed(() => {
  const d = props.data
  if (!d) return []
  const filtered = store.sharedFilter.value
  const years = d.category_impact.map((c) => c.year)
  const cats = d.impact_categories
  const z = cats.map((cat) =>
    d.category_impact.map((c) => {
      const item = c.items.find((i) => i.category === cat)
      return item ? item.yoy : 0
    })
  )
  const xgap = filtered ? cats.map((cat) => (store.isFilteredCategory(cat) ? 3 : 1)) : 1
  const ygap = filtered ? cats.map((cat) => (store.isFilteredCategory(cat) ? 3 : 1)) : 1
  return [
    {
      z,
      x: years.map((y) => String(y)),
      y: cats,
      type: 'heatmap',
      xgap,
      ygap,
      colorscale: [
        [0, '#E57373'],
        [0.45, '#FFFFFF'],
        [0.55, '#FFFFFF'],
        [1, '#7CB342'],
      ],
      zmin: -40,
      zmax: 40,
      cmid: 0,
      hovertemplate: '<b>%{y}</b><br>%{x}年<br>同比 %{z:+.1f}%<extra></extra>',
      colorbar: {
        title: { text: '同比%', font: { size: 10, color: '#6d5546' } },
        tickfont: { size: 9, color: '#a1887f' },
        len: 0.85,
      },
      text: z.map((row) => row.map((v) => (v >= 0 ? '+' : '') + v.toFixed(1) + '%')),
      texttemplate: '%{text}',
      textfont: { size: 11, color: '#4e342e' },
    },
  ]
})

const impactLayout = computed(() => {
  const d = props.data
  if (!d) return {}
  const filtered = store.sharedFilter.value
  const cats = d.impact_categories
  const tickfont = cats.map((cat) => ({
    size: filtered ? (store.isFilteredCategory(cat) ? 13 : 10) : 11,
    color: filtered ? (store.isFilteredCategory(cat) ? '#E5704F' : '#8d6e63') : '#6d5546',
    weight: filtered ? (store.isFilteredCategory(cat) ? 'bold' : 'normal') : 'normal',
  }))
  const extraShapes = []
  if (filtered) {
    cats.forEach((cat, catIdx) => {
      if (store.isFilteredCategory(cat)) {
        extraShapes.push({
          type: 'rect',
          xref: 'x',
          yref: 'y',
          x0: -0.5,
          x1: 0.48 + d.category_impact.length,
          y0: catIdx - 0.48,
          y1: catIdx + 0.48,
          fillcolor: '#E5704F22',
          line: { color: '#E5704F', width: 3 },
          layer: 'above',
        })
      }
    })
  }
  return plotLayout({
    height: 400,
    margin: { l: 96, r: 24, t: 16, b: 40 },
    yaxis: { automargin: true, tickfont, tickmode: 'array', tickvals: cats.map((_, i) => i), ticktext: cats },
    xaxis: { tickfont: { size: 12, color: '#6d5546' } },
    shapes: extraShapes,
  })
})

function onDataClick(payload) {
  emit('data-click', payload)
}
</script>

<template>
  <div v-if="data">
    <v-row>
      <v-col cols="12" md="7">
        <div class="chart-hint mb-1">出生率与市场规模趋势（粉色带为特殊年份）</div>
        <PlotChart
          :data="trendTraces"
          :layout="trendLayout"
          :chart-title="'出生率波动与市场规模趋势（2010-2024）'"
          height="380px"
        />
      </v-col>
      <v-col cols="12" md="5">
        <div class="chart-hint mb-1">特殊年份细分品类同比影响</div>
        <PlotChart
          :data="impactTrace"
          :layout="impactLayout"
          :chart-title="'特殊年份对细分品类的同比影响热力图'"
          height="400px"
          :clickable="true"
          @data-click="onDataClick"
        />
      </v-col>
    </v-row>
  </div>
  <v-skeleton-loader v-else type="image" height="400" />
</template>

<style scoped>
.chart-hint {
  font-size: 0.82rem;
  color: var(--c-ink-soft);
  font-weight: 500;
}
</style>
