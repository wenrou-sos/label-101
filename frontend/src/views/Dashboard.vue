<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useDisplay } from 'vuetify'
import { useDashboardStore } from '../stores/dashboard'
import AppHeader from '../components/layout/AppHeader.vue'
import SideNav from '../components/layout/SideNav.vue'
import SectionCard from '../components/layout/SectionCard.vue'
import OverviewSection from '../components/sections/OverviewSection.vue'
import AgeStageSection from '../components/sections/AgeStageSection.vue'
import CategoryDecisionSection from '../components/sections/CategoryDecisionSection.vue'
import CityTierSection from '../components/sections/CityTierSection.vue'
import LoyaltySection from '../components/sections/LoyaltySection.vue'
import SpecialYearSection from '../components/sections/SpecialYearSection.vue'

const store = useDashboardStore()
const { mdAndUp } = useDisplay()

const sections = [
  { id: 'overview', title: '总览看板', icon: 'mdi-view-dashboard', color: '#FF8A65' },
  { id: 'ageStage', title: '月龄阶段消费', icon: 'mdi-timeline-clock-outline', color: '#7CB342' },
  { id: 'decision', title: '品类决策因素', icon: 'mdi-chart-arc', color: '#EC9BAE' },
  { id: 'cityTier', title: '城市层级差异', icon: 'mdi-map-marker-radius', color: '#64B5F6' },
  { id: 'loyalty', title: '复购品牌忠诚度', icon: 'mdi-repeat-variant', color: '#A1887F' },
  { id: 'specialYear', title: '特殊年份影响', icon: 'mdi-calendar-star', color: '#FFB74D' },
]

const activeId = ref('overview')
let observer = null
const sectionRefs = {}

function setRef(id) {
  return (el) => {
    if (el) sectionRefs[id] = el
  }
}

function navigate(id) {
  const el = sectionRefs[id] || document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  activeId.value = id
}

function setupObserver() {
  observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
      if (visible[0]) {
        const id = visible[0].target.getAttribute('data-id')
        if (id) activeId.value = id
      }
    },
    { rootMargin: '-30% 0px -55% 0px', threshold: [0, 0.25, 0.5] }
  )
  Object.values(sectionRefs).forEach((el) => el && observer.observe(el))
}

async function refresh() {
  store.loadedAt = null
  store.error = null
  await store.fetchAll()
  await nextTick()
  setupObserver()
}

onMounted(async () => {
  await store.fetchAll()
  await nextTick()
  setupObserver()
})

onBeforeUnmount(() => {
  if (observer) observer.disconnect()
})
</script>

<template>
  <div>
    <AppHeader :loading="store.loading" @refresh="refresh" />

    <v-navigation-drawer
      v-if="mdAndUp"
      permanent
      width="236"
      class="side-drawer"
      location="left"
    >
      <SideNav :sections="sections" :active-id="activeId" @navigate="navigate" />
    </v-navigation-drawer>

    <v-main class="main-area">
      <v-alert
        v-if="store.error"
        type="error"
        variant="tonal"
        class="ma-4"
        closable
      >
        数据加载失败：{{ store.error }}，请确认后端服务已启动后点击刷新。
      </v-alert>

      <div class="nav-chips-mobile" v-if="!mdAndUp">
        <v-chip
          v-for="s in sections"
          :key="s.id"
          :color="activeId === s.id ? s.color : ''"
          :variant="activeId === s.id ? 'flat' : 'tonal'"
          size="small"
          @click="navigate(s.id)"
          class="ma-1"
        >
          {{ s.title }}
        </v-chip>
      </div>

      <v-container class="content-wrap" :fluid="!mdAndUp">
        <section class="hero float-in">
          <div class="hero-eyebrow">
            <v-icon icon="mdi-chart-box-outline" size="14" color="#FF8A65" />
            全周期 · 全品类 · 全城市层级 数据洞察
          </div>
          <h1 class="hero-title brand-gradient-text">母婴市场消费分析看板</h1>
          <p class="hero-desc">
            覆盖孕期囤货至 3-6 岁六大月龄阶段，洞察五大核心品类购买决策、城市层级消费差异、
            高频消耗品品牌忠诚度，并解析疫情与龙宝宝等特殊年份对母婴市场的影响趋势。
          </p>
          <div class="hero-tags">
            <span class="hero-tag"><v-icon icon="mdi-chart-pie" size="14" />6 月龄阶段</span>
            <span class="hero-tag"><v-icon icon="mdi-shield-check" size="14" />5 核心品类</span>
            <span class="hero-tag"><v-icon icon="mdi-map" size="14" />2 城市层级</span>
            <span class="hero-tag"><v-icon icon="mdi-chart-bell-curve" size="14" />生存分析</span>
          </div>
        </section>

        <div
          v-for="s in sections"
          :key="s.id"
          :ref="setRef(s.id)"
          :data-id="s.id"
          class="section-anchor"
        >
          <SectionCard
            :title="s.title"
            :icon="s.icon"
            :icon-color="s.color"
            class="mb-6"
          >
            <OverviewSection v-if="s.id === 'overview'" :data="store.overview" :loading="store.loading" />
            <AgeStageSection v-else-if="s.id === 'ageStage'" :data="store.ageStage" />
            <CategoryDecisionSection v-else-if="s.id === 'decision'" :data="store.decision" />
            <CityTierSection v-else-if="s.id === 'cityTier'" :data="store.cityTier" />
            <LoyaltySection v-else-if="s.id === 'loyalty'" :data="store.loyalty" />
            <SpecialYearSection v-else-if="s.id === 'specialYear'" :data="store.specialYear" />
          </SectionCard>
        </div>

        <footer class="foot">
          <span>母婴市场消费洞察看板 · 基于 Python + Vue3 + Vuetify + Plotly.js 构建</span>
          <span class="foot-dot">·</span>
          <span>模拟数据仅供分析演示</span>
        </footer>
      </v-container>
    </v-main>
  </div>
</template>

<style scoped>
.side-drawer {
  background: rgba(255, 248, 243, 0.6) !important;
  backdrop-filter: blur(8px);
  border-right: 1px solid var(--c-line) !important;
}
.main-area {
  background: transparent;
}
.content-wrap {
  max-width: 1320px;
  padding-top: 28px;
  padding-bottom: 60px;
}
.section-anchor {
  scroll-margin-top: 92px;
}
.hero {
  margin-bottom: 32px;
  padding: 8px 4px;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  letter-spacing: 1px;
  color: var(--c-ink-soft);
  background: #fff0e8;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: 600;
}
.hero-title {
  font-family: var(--font-serif);
  font-weight: 900;
  font-size: clamp(2rem, 4vw, 3rem);
  margin: 16px 0 12px;
  line-height: 1.15;
}
.hero-desc {
  max-width: 820px;
  font-size: 0.98rem;
  line-height: 1.7;
  color: var(--c-ink-soft);
  margin: 0 0 18px;
}
.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--c-ink);
  background: #fff;
  border: 1px solid var(--c-line);
  padding: 6px 14px;
  border-radius: 20px;
  box-shadow: 0 6px 16px -12px rgba(166, 92, 62, 0.4);
}
.nav-chips-mobile {
  display: flex;
  overflow-x: auto;
  padding: 10px 12px;
  background: rgba(255, 248, 243, 0.8);
  position: sticky;
  top: 72px;
  z-index: 5;
  border-bottom: 1px solid var(--c-line);
}
.foot {
  text-align: center;
  color: #b39a8c;
  font-size: 0.82rem;
  padding: 24px 0 8px;
}
.foot-dot {
  margin: 0 8px;
}
</style>
