<script setup>
import { computed } from 'vue'
import PlotChart from '../charts/PlotChart.vue'
import KpiCard from '../KpiCard.vue'
import { PALETTE, COLOR, plotLayout } from '../../constants/charts'

const props = defineProps({
  data: { type: Object, default: null },
  loading: { type: Boolean, default: false },
})

const birthTrace = computed(() => {
  const d = props.data
  if (!d) return []
  const years = d.birth_trend.map((r) => r.year)
  const counts = d.birth_trend.map((r) => r.birth_count)
  const special = d.birth_trend.filter((r) => r.special_tag)
  return [
    {
      x: years,
      y: counts,
      mode: 'lines+markers',
      line: { color: COLOR.coral, width: 3, shape: 'spline' },
      marker: {
        size: 8,
        color: counts.map((_, i) =>
          d.birth_trend[i].special_tag ? COLOR.rose : COLOR.coral
        ),
        line: { color: '#fff', width: 2 },
      },
      fill: 'tozeroy',
      fillcolor: 'rgba(255,138,101,0.12)',
      name: '出生人口',
      hovertemplate: '<b>%{x}年</b><br>出生 %{y} 万<extra></extra>',
    },
    {
      x: special.map((r) => r.year),
      y: special.map((r) => r.birth_count),
      mode: 'markers',
      marker: { size: 15, color: COLOR.rose, symbol: 'star', line: { color: '#fff', width: 1.5 } },
      name: '特殊年份',
      hovertemplate: '<b>%{x}年</b> %{text}<br>出生 %{y} 万<extra></extra>',
      text: special.map((r) => r.special_tag),
      showlegend: false,
    },
  ]
})

const birthLayout = computed(() =>
  plotLayout({
    height: 360,
    margin: { l: 50, r: 24, t: 20, b: 40 },
    xaxis: { title: '', gridcolor: '#F0DDD2', zeroline: false },
    yaxis: { title: '出生人口（万）', gridcolor: '#F0DDD2', zeroline: false },
    showlegend: false,
  })
)
</script>

<template>
  <div>
    <v-row class="mb-2" dense>
      <v-col cols="12" sm="6" md="3" v-for="k in data?.kpis || []" :key="k.key">
        <KpiCard :kpi="k" />
      </v-col>
      <template v-if="loading && !data">
        <v-col cols="12" sm="6" md="3" v-for="i in 4" :key="i">
          <v-skeleton-loader type="card" height="120" />
        </v-col>
      </template>
    </v-row>
    <PlotChart
      v-if="data"
      :data="birthTrace"
      :layout="birthLayout"
      height="360px"
    />
  </div>
</template>
