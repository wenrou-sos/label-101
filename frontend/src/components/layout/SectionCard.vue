<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' },
  iconColor: { type: String, default: '#FF8A65' },
})
</script>

<template>
  <v-card class="chart-card section-wrap pa-6 pa-md-7 h-100" flat>
    <div class="d-flex align-center mb-5">
      <div class="section-icon me-3" :style="{ background: iconColor + '22' }">
        <v-icon :icon="icon" :color="iconColor" size="22" />
      </div>
      <div>
        <h3 class="section-title ma-0">{{ title }}</h3>
        <p class="section-subtitle ma-0" v-if="subtitle">{{ subtitle }}</p>
      </div>
    </div>
    <slot />
  </v-card>
</template>

<style scoped>
.section-wrap {
  display: flex;
  flex-direction: column;
}
.section-icon {
  width: 44px;
  height: 44px;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
</style>
