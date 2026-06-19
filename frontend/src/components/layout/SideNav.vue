<script setup>
defineProps({
  sections: { type: Array, required: true },
  activeId: { type: String, default: '' },
})
const emit = defineEmits(['navigate'])
</script>

<template>
  <nav class="side-nav">
    <div class="nav-label">分析模块</div>
    <v-list density="compact" class="nav-list" nav>
      <v-list-item
        v-for="s in sections"
        :key="s.id"
        :active="activeId === s.id"
        @click="emit('navigate', s.id)"
        rounded="lg"
        class="nav-item mb-1"
      >
        <template v-slot:prepend>
          <span class="nav-dot" :style="{ background: s.color }"></span>
        </template>
        <v-list-item-title class="nav-text">{{ s.title }}</v-list-item-title>
        <template v-slot:append>
          <v-icon
            :icon="activeId === s.id ? 'mdi-chevron-right' : ''"
            :color="s.color"
            size="18"
          />
        </template>
      </v-list-item>
    </v-list>
    <div class="nav-foot">
      <v-icon icon="mdi-baby-carriage" color="#FF8A65" size="22" />
      <div class="nav-foot-text">母婴消费洞察</div>
      <div class="nav-foot-sub">数据更新于 2024</div>
    </div>
  </nav>
</template>

<style scoped>
.side-nav {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 18px 12px;
}
.nav-label {
  font-size: 0.72rem;
  letter-spacing: 2px;
  color: #b39a8c;
  padding: 4px 12px 12px;
  text-transform: uppercase;
}
.nav-list {
  flex: 1;
}
.nav-item {
  font-size: 0.92rem;
  color: var(--c-ink-soft);
}
.nav-item.v-list-item--active {
  background: #fff0e8 !important;
  color: var(--c-ink) !important;
  font-weight: 600;
}
.nav-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 4px;
}
.nav-text {
  font-size: 0.9rem;
}
.nav-foot {
  margin-top: 12px;
  padding: 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, #fff0e8 0%, #fde4ec 100%);
  text-align: center;
}
.nav-foot-text {
  font-family: var(--font-serif);
  font-weight: 700;
  color: var(--c-ink);
  margin-top: 6px;
  font-size: 0.92rem;
}
.nav-foot-sub {
  font-size: 0.72rem;
  color: #b39a8c;
  margin-top: 2px;
}
</style>
