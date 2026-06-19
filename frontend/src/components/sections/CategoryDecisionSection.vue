<script setup>
import { computed } from 'vue'
import PlotChart from '../charts/PlotChart.vue'
import { PALETTE, COLOR, plotLayout } from '../../constants/charts'
import { useDashboardStore } from '../../stores/dashboard'

const props = defineProps({
  data: { type: Object, default: null },
})

const emit = defineEmits(['data-click'])

const store = useDashboardStore()

const cards = computed(() => {
  const d = props.data
  if (!d) return []
  return d.categories.map((c, i) => {
    const color = PALETTE[i % PALETTE.length]
    const all = c.all_factors
    const isMatch = store.isFilteredCategory(c.category)
    const lineWidth = isMatch === true ? 4 : isMatch === false ? 1.5 : 2.5
    const opacity = isMatch === false ? 0.35 : 1
    const markerSize = isMatch === true ? 8 : isMatch === false ? 4 : 6
    const radar = [
      {
        type: 'scatterpolar',
        r: [...all.map((f) => f.weight), all[0].weight],
        theta: [...all.map((f) => f.factor), all[0].factor],
        fill: 'toself',
        fillcolor: color + (isMatch === true ? '55' : isMatch === false ? '15' : '33'),
        line: { color, width: lineWidth },
        marker: { size: markerSize, color, opacity },
        opacity,
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
      isHighlighted: isMatch === true,
      isDimmed: isMatch === false,
    }
  })
})

function onDataClick(payload) {
  emit('data-click', payload)
}
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
        <v-card
          class="chart-card pa-5 h-100 d-flex flex-column"
          flat
          :class="{
            'card-highlighted': card.isHighlighted,
            'card-dimmed': card.isDimmed,
          }"
          :style="card.isHighlighted ? {
            borderColor: card.color,
            boxShadow: '0 0 0 2px ' + card.color + '33, 0 12px 32px -8px ' + card.color + '66',
          } : {}"
        >
          <div class="d-flex align-center mb-2">
            <span class="cat-dot" :style="{ background: card.color }"></span>
            <h4 class="cat-title">{{ card.category }}</h4>
            <v-chip
              v-if="card.isHighlighted"
              size="x-small"
              color="#E5704F"
              class="ml-auto"
              density="compact"
            >
              <v-icon start icon="mdi-check-circle-outline" size="12" />
              已选中
            </v-chip>
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
                opacity: card.isDimmed ? 0.4 : 1,
              }"
            >
              <span class="rank">{{ i + 1 }}</span>{{ t.factor }} {{ t.weight }}%
            </span>
          </div>
          <PlotChart
            :data="card.trace"
            :layout="card.layout"
            :chart-title="card.category + ' · 购买决策因素雷达图'"
            height="280px"
            :clickable="true"
            @data-click="onDataClick"
          />
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
  transition: transform 0.2s ease;
}
.card-highlighted .cat-dot {
  transform: scale(1.25);
}
.cat-title {
  font-family: var(--font-serif);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--c-ink);
  margin: 0;
  transition: color 0.2s ease;
}
.card-highlighted .cat-title {
  color: #E5704F;
}
.card-dimmed {
  opacity: 0.55;
  filter: grayscale(0.3);
}
.card-highlighted {
  border: 2px solid transparent;
  transform: translateY(-2px);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
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
  transition: opacity 0.2s ease;
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
.card-highlighted .rank {
  background: #ffffff;
}
</style>
