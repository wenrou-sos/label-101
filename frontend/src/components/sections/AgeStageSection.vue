<script setup>
import { ref, computed } from 'vue'
import PlotChart from '../charts/PlotChart.vue'
import { PALETTE, COLOR, plotLayout } from '../../constants/charts'
import { useDashboardStore } from '../../stores/dashboard'

const props = defineProps({
  data: { type: Object, default: null },
})

const emit = defineEmits(['data-click'])

const store = useDashboardStore()

const activeStage = ref(0)

const stages = computed(() => props.data?.stages || [])
const activeShare = computed(() => {
  const s = stages.value[activeStage.value]
  return s ? props.data.category_share[s] || [] : []
})

const donutTrace = computed(() => {
  const share = activeShare.value
  const filtered = store.sharedFilter.value
  const labels = share.map((r) => r.category)
  const values = share.map((r) => r.amount)
  const pull = labels.map((cat) =>
    filtered ? (store.isFilteredCategory(cat) ? 0.12 : 0) : 0
  )
  const markerLineWidth = labels.map((cat) =>
    filtered ? (store.isFilteredCategory(cat) ? 4 : 1.5) : 2
  )
  const markerLineColor = labels.map((cat) =>
    filtered ? (store.isFilteredCategory(cat) ? '#E5704F' : '#fff') : '#fff'
  )
  const opacity = labels.map((cat) =>
    filtered ? (store.isFilteredCategory(cat) ? 1 : 0.4) : 1
  )
  const textfontSize = labels.map((cat) =>
    filtered ? (store.isFilteredCategory(cat) ? 13 : 10) : 11
  )
  return [
    {
      labels,
      values,
      type: 'pie',
      hole: 0.62,
      pull,
      marker: {
        colors: PALETTE,
        line: { color: markerLineColor, width: markerLineWidth },
      },
      textinfo: 'percent',
      texttemplate: '%{label}<br>%{percent}',
      textposition: 'outside',
      textfont: { size: textfontSize, color: '#4e342e' },
      hovertemplate: '<b>%{label}</b><br>金额 %{value:,.0f} 元<br>占比 %{percent}<extra></extra>',
      sort: false,
      opacity,
    },
  ]
})

const donutLayout = computed(() => {
  const filtered = store.sharedFilter.value
  return plotLayout({
    height: 380,
    margin: { l: 12, r: 12, t: 10, b: 10 },
    showlegend: false,
    annotations: [
      {
        text: `<span style="font-size:13px;color:${filtered ? '#E5704F' : '#6d5546'}">${stages.value[activeStage.value] || ''}</span><br><span style="font-size:11px;color:#a1887f">类目金额占比</span>`,
        showarrow: false,
        font: { color: '#4e342e' },
      },
    ],
  })
})

const trendTrace = computed(() => {
  const d = props.data
  if (!d) return []
  const barColors = d.avg_order_trend.map((_, i) => PALETTE[i % PALETTE.length])
  return [
    {
      x: d.avg_order_trend.map((r) => r.stage),
      y: d.avg_order_trend.map((r) => r.avg_order),
      type: 'bar',
      marker: {
        color: barColors,
        line: { color: '#fff', width: 1.5 },
        radius: 8,
      },
      hovertemplate: '<b>%{x}</b><br>客单价 %{y:.0f} 元<extra></extra>',
    },
  ]
})

const trendLayout = computed(() => {
  return plotLayout({
    height: 380,
    margin: { l: 56, r: 24, t: 20, b: 40 },
    xaxis: { gridcolor: '#F0DDD2', zeroline: false },
    yaxis: { title: '客单价（元）', gridcolor: '#F0DDD2', zeroline: false },
    showlegend: false,
  })
})

function onDataClick(payload) {
  emit('data-click', payload)
}
</script>

<template>
  <div v-if="data">
    <div class="d-flex flex-wrap gap-2 mb-5">
      <v-chip
        v-for="(s, i) in stages"
        :key="s"
        :color="i === activeStage ? 'primary' : ''"
        :variant="i === activeStage ? 'flat' : 'tonal'"
        size="small"
        @click="activeStage = i"
        class="stage-chip"
      >
        <v-icon start :icon="i === activeStage ? 'mdi-baby-face' : 'mdi-circle-small'" size="14" />
        {{ s }}
      </v-chip>
    </div>
    <v-row>
      <v-col cols="12" md="6">
        <PlotChart
          :data="donutTrace"
          :layout="donutLayout"
          :chart-title="stages[activeStage] + ' · 类目金额占比'"
          height="380px"
          :clickable="true"
          @data-click="onDataClick"
        />
      </v-col>
      <v-col cols="12" md="6">
        <PlotChart
          :data="trendTrace"
          :layout="trendLayout"
          :chart-title="'各月龄阶段客单价趋势'"
          height="380px"
        />
      </v-col>
    </v-row>
  </div>
  <v-skeleton-loader v-else type="image" height="380" />
</template>

<style scoped>
.gap-2 {
  gap: 8px;
}
.stage-chip {
  font-weight: 600;
}
</style>
