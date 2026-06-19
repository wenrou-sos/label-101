<script setup>
import { computed } from 'vue'
import PlotChart from '../charts/PlotChart.vue'
import { COLOR, plotLayout } from '../../constants/charts'

const props = defineProps({
  data: { type: Object, default: null },
})

const heatTrace = computed(() => {
  const d = props.data
  if (!d) return []
  const cats = d.preference.map((r) => r.category)
  const z = d.preference.map((r) => d.tiers.map((t) => r[t]))
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
      text: z.map((row) => row.map((v) => v.toFixed(0))),
      texttemplate: '%{text}',
      textfont: { size: 11, color: '#4e342e' },
    },
  ]
})

const heatLayout = computed(() =>
  plotLayout({
    height: 460,
    margin: { l: 110, r: 24, t: 16, b: 40 },
    yaxis: { automargin: true, tickfont: { size: 11 } },
    xaxis: { tickfont: { size: 12, color: '#6d5546' } },
  })
)

const tierColor = { 一线城市: COLOR.coral, 二线城市: COLOR.mint, 下沉市场: COLOR.sky }

const boxTraces = computed(() => {
  const d = props.data
  if (!d) return []
  const traces = []
  for (const tier of d.tiers) {
    const arr = d.price_distribution[tier]
    if (!arr) continue
    traces.push({
      type: 'box',
      x: arr.map((r) => r.category),
      q1: arr.map((r) => r.q1),
      median: arr.map((r) => r.median),
      q3: arr.map((r) => r.q3),
      lowerfence: arr.map((r) => r.min),
      upperfence: arr.map((r) => r.max),
      name: tier,
      marker: { color: tierColor[tier] },
      line: { color: tierColor[tier], width: 2 },
      fillcolor: tierColor[tier] + '33',
      boxpoints: false,
      offsetgroup: tier,
    })
  }
  return traces
})

const boxLayout = computed(() =>
  plotLayout({
    height: 380,
    margin: { l: 56, r: 24, t: 16, b: 90 },
    boxmode: 'group',
    xaxis: { tickangle: -35, gridcolor: '#F0DDD2', tickfont: { size: 10 } },
    yaxis: { title: '价格（元）', gridcolor: '#F0DDD2' },
    legend: { orientation: 'h', y: -0.42, font: { size: 11 } },
  })
)
</script>

<template>
  <div v-if="data">
    <v-row>
      <v-col cols="12" md="6">
        <div class="chart-hint mb-1">品类偏好热力图 · 人均消费（元/人）</div>
        <PlotChart :data="heatTrace" :layout="heatLayout" height="460px" />
      </v-col>
      <v-col cols="12" md="6">
        <div class="chart-hint mb-1">价格带分布箱线图 · 一线 / 二线 / 下沉市场</div>
        <PlotChart :data="boxTraces" :layout="boxLayout" height="380px" />
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
