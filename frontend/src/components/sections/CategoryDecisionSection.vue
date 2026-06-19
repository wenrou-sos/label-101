<script setup>
import { computed } from 'vue'
import PlotChart from '../charts/PlotChart.vue'
import { PALETTE, COLOR, plotLayout } from '../../constants/charts'

const props = defineProps({
  data: { type: Object, default: null },
})

const cards = computed(() => {
  const d = props.data
  if (!d) return []
  return d.categories.map((c, i) => {
    const color = PALETTE[i % PALETTE.length]
    const all = c.all_factors
    const radar = [
      {
        type: 'scatterpolar',
        r: [...all.map((f) => f.weight), all[0].weight],
        theta: [...all.map((f) => f.factor), all[0].factor],
        fill: 'toself',
        fillcolor: color + '33',
        line: { color, width: 2.5 },
        marker: { size: 6, color },
        name: c.category,
        hovertemplate: '<b>%{theta}</b><br>权重 %{r}%<extra></extra>',
      },
    ]
    const layout = plotLayout({
      height: 280,
      margin: { l: 28, r: 28, t: 10, b: 10 },
      showlegend: false,
      polar: {
        bgcolor: 'rgba(0,0,0,0)',
        radialaxis: {
          range: [0, 50],
          tickfont: { size: 9, color: '#b39a8c' },
          gridcolor: '#F0DDD2',
          tickcolor: '#F0DDD2',
        },
        angularaxis: {
          tickfont: { size: 11, color: '#6d5546' },
          gridcolor: '#F0DDD2',
          linecolor: '#F0DDD2',
        },
      },
    })
    return {
      category: c.category,
      color,
      top3: c.factors,
      trace: radar,
      layout,
    }
  })
})
</script>

<template>
  <div v-if="data">
    <v-row>
      <v-col
        v-for="card in cards"
        :key="card.category"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card class="chart-card pa-5 h-100 d-flex flex-column" flat>
          <div class="d-flex align-center mb-2">
            <span class="cat-dot" :style="{ background: card.color }"></span>
            <h4 class="cat-title">{{ card.category }}</h4>
          </div>
          <div class="top3-row mb-1">
            <span
              v-for="(t, i) in card.top3"
              :key="t.factor"
              class="top3-chip"
              :style="{
                border: '1px solid ' + card.color + '55',
                color: i === 0 ? card.color : '#6d5546',
                background: i === 0 ? card.color + '1a' : '#fff7f3',
              }"
            >
              <span class="rank">{{ i + 1 }}</span>{{ t.factor }} {{ t.weight }}%
            </span>
          </div>
          <PlotChart :data="card.trace" :layout="card.layout" height="280px" />
        </v-card>
      </v-col>
    </v-row>
  </div>
  <v-skeleton-loader v-else type="card" height="320" />
</template>

<style scoped>
.cat-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}
.cat-title {
  font-family: var(--font-serif);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--c-ink);
  margin: 0;
}
.top3-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.top3-chip {
  display: inline-flex;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 20px;
}
.rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #ffffffcc;
  font-size: 0.66rem;
  font-weight: 700;
  margin-right: 4px;
  color: #a1887f;
}
</style>
