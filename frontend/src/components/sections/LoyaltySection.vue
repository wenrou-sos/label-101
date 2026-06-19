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

const catColor = { 纸尿裤: COLOR.coral, 奶粉: COLOR.mint }

const survivalTraces = computed(() => {
  const d = props.data
  if (!d) return []
  const filtered = store.sharedFilter.value
  const traces = []
  for (const cat of d.categories) {
    const curve = d.survival_curves[cat]
    const isMatch = store.isFilteredCategory(cat)
    const lineWidth = isMatch === true ? 5 : isMatch === false ? 1.5 : 3
    const markerSize = isMatch === true ? 8 : isMatch === false ? 3 : 5
    const opacity = isMatch === false ? 0.4 : 1
    const dash = isMatch === false ? 'dash' : 'solid'
    traces.push({
      x: curve.map((p) => p.month),
      y: curve.map((p) => p.survival),
      mode: 'lines+markers',
      name: cat,
      line: { color: catColor[cat], width: lineWidth, shape: 'spline', dash },
      marker: { size: markerSize, color: catColor[cat], opacity },
      fill: isMatch !== false ? 'tozeroy' : 'none',
      fillcolor: catColor[cat] + (isMatch === true ? '35' : '1f'),
      opacity,
      hovertemplate: '<b>' + cat + '</b><br>第 %{x} 月<br>留存率 %{y:.1%}<extra></extra>',
    })
  }
  return traces
})

const survivalLayout = computed(() => {
  const d = props.data
  const filtered = store.sharedFilter.value
  return plotLayout({
    height: 360,
    margin: { l: 52, r: 24, t: 16, b: 40 },
    xaxis: { title: '使用月数', gridcolor: '#F0DDD2', dtick: 3 },
    yaxis: {
      title: '品牌留存率',
      gridcolor: '#F0DDD2',
      tickformat: '.0%',
      range: [0, 1.02],
    },
    legend: { orientation: 'h', y: 1.12, x: 0.3, font: { size: filtered ? 13 : 12, color: '#4e342e' } },
    hovermode: 'x unified',
  })
})

const switchTrace = computed(() => {
  const d = props.data
  if (!d) return []
  const dist = d.switch_time_distribution
  return [
    {
      x: dist.map((r) => r.range),
      y: dist.map((r) => r.count),
      type: 'bar',
      marker: {
        color: dist.map((r) => r.count),
        colorscale: [[0, '#FFD0B8'], [1, '#FF8A65']],
        line: { color: '#fff', width: 1.5 },
      },
      hovertemplate: '<b>%{x}</b><br>换品牌用户 %{y} 人<extra></extra>',
    },
  ]
})

const switchLayout = computed(() =>
  plotLayout({
    height: 360,
    margin: { l: 52, r: 24, t: 16, b: 40 },
    xaxis: { gridcolor: '#F0DDD2', tickangle: -15 },
    yaxis: { title: '换品牌人数', gridcolor: '#F0DDD2' },
    showlegend: false,
  })
)

const brandTraces = computed(() => {
  const d = props.data
  if (!d) return []
  const filtered = store.sharedFilter.value
  const labels = []
  const values = []
  const colors = []
  const lineWidths = []
  const opacities = []
  const textSizes = []
  for (const cat of d.categories) {
    for (const b of d.brand_stay[cat]) {
      labels.push(`${b.brand} · ${cat}`)
      values.push(b.avg_stay_months)
      colors.push(catColor[cat])
      const isMatch = store.isFilteredCategory(cat)
      lineWidths.push(isMatch === true ? 3 : isMatch === false ? 1 : 1.5)
      opacities.push(isMatch === false ? 0.4 : 1)
      textSizes.push(isMatch === true ? 12 : isMatch === false ? 10 : 11)
    }
  }
  return [
    {
      type: 'bar',
      orientation: 'h',
      y: labels,
      x: values,
      marker: {
        color: colors,
        line: { color: '#fff', width: lineWidths },
      },
      opacity: opacities,
      textposition: 'auto',
      insidetextfont: { size: textSizes, color: '#fff', weight: 'bold' },
      hovertemplate: '<b>%{y}</b><br>平均停留 %{x} 个月<extra></extra>',
    },
  ]
})

const brandLayout = computed(() => {
  const d = props.data
  const filtered = store.sharedFilter.value
  const labels = []
  for (const cat of d?.categories || []) {
    for (const b of d?.brand_stay?.[cat] || []) {
      labels.push(`${b.brand} · ${cat}`)
    }
  }
  const tickfont = labels.map((l) => {
    const cat = l.split(' · ')[1]
    const isMatch = store.isFilteredCategory(cat)
    return {
      size: filtered ? (isMatch ? 13 : 10) : 11,
      color: filtered ? (isMatch ? '#E5704F' : '#8d6e63') : '#6d5546',
      weight: filtered ? (isMatch ? 'bold' : 'normal') : 'normal',
    }
  })
  return plotLayout({
    height: 360,
    margin: { l: 130, r: 24, t: 16, b: 40 },
    yaxis: { gridcolor: '#F0DDD2', automargin: true, autorange: 'reversed', tickfont },
    xaxis: { title: '平均停留月数', gridcolor: '#F0DDD2' },
    showlegend: false,
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
        <div class="chart-hint mb-1">品牌留存生存曲线（Kaplan-Meier 估计）</div>
        <PlotChart
          :data="survivalTraces"
          :layout="survivalLayout"
          :chart-title="'纸尿裤 / 奶粉 品牌留存生存曲线'"
          height="360px"
          :clickable="true"
          @data-click="onDataClick"
        />
      </v-col>
      <v-col cols="12" md="5">
        <div class="chart-hint mb-1">换品牌时间分布</div>
        <PlotChart
          :data="switchTrace"
          :layout="switchLayout"
          :chart-title="'高频消耗品换品牌时间分布'"
          height="360px"
        />
      </v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col cols="12">
        <div class="chart-hint mb-1">各品牌平均停留时长</div>
        <PlotChart
          :data="brandTraces"
          :layout="brandLayout"
          :chart-title="'各品牌平均停留时长（按月）'"
          height="360px"
          :clickable="true"
          @data-click="onDataClick"
        />
      </v-col>
    </v-row>
  </div>
  <v-skeleton-loader v-else type="image" height="360" />
</template>

<style scoped>
.chart-hint {
  font-size: 0.82rem;
  color: var(--c-ink-soft);
  font-weight: 500;
}
</style>
