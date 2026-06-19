<script setup>
defineProps({
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['refresh'])
</script>

<template>
  <v-app-bar flat class="app-header" height="72">
    <div class="d-flex align-center h-100 px-5 px-md-8 w-100">
      <div class="d-flex align-center">
        <div class="logo-badge">
          <v-icon icon="mdi-baby-face-outline" color="#fff" size="24" />
        </div>
        <div class="ms-3">
          <div class="brand-title brand-gradient-text">母婴消费洞察</div>
          <div class="brand-sub">Maternal & Infant Market Insight</div>
        </div>
      </div>
      <v-spacer />
      <div class="d-none d-md-flex align-center me-3">
        <v-chip variant="tonal" color="primary" size="small" class="me-2">
          <v-icon start icon="mdi-calendar-range" size="15" />2010 — 2024
        </v-chip>
        <v-chip variant="tonal" color="secondary" size="small">
          <v-icon start icon="mdi-database" size="15" />模拟数据集
        </v-chip>
      </div>
      <v-btn
        variant="flat"
        color="primary"
        :loading="loading"
        @click="emit('refresh')"
        class="refresh-btn"
      >
        <v-icon start icon="mdi-refresh" />刷新
      </v-btn>
    </div>
  </v-app-bar>
</template>

<style scoped>
.app-header {
  background: rgba(255, 248, 243, 0.85) !important;
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--c-line) !important;
}
.logo-badge {
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: linear-gradient(135deg, #ff8a65 0%, #ec9bae 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px -8px rgba(255, 138, 101, 0.6);
}
.brand-title {
  font-family: var(--font-serif);
  font-weight: 900;
  font-size: 1.35rem;
  letter-spacing: 1px;
}
.brand-sub {
  font-size: 0.66rem;
  letter-spacing: 1.5px;
  color: #b39a8c;
  text-transform: uppercase;
}
.refresh-btn {
  color: #fff !important;
  font-weight: 600;
}
</style>
