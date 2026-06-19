import { defineStore } from 'pinia'
import {
  getOverview,
  getAgeStageConsumption,
  getCategoryDecisionFactors,
  getCityTierComparison,
  getLoyaltySurvival,
  getSpecialYearImpact,
} from '../api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    overview: null,
    ageStage: null,
    decision: null,
    cityTier: null,
    loyalty: null,
    specialYear: null,
    loading: false,
    error: null,
    loadedAt: null,
  }),
  actions: {
    async fetchAll() {
      if (this.loadedAt) return
      this.loading = true
      this.error = null
      try {
        const [
          overview,
          ageStage,
          decision,
          cityTier,
          loyalty,
          specialYear,
        ] = await Promise.all([
          getOverview(),
          getAgeStageConsumption(),
          getCategoryDecisionFactors(),
          getCityTierComparison(),
          getLoyaltySurvival(),
          getSpecialYearImpact(),
        ])
        this.overview = overview
        this.ageStage = ageStage
        this.decision = decision
        this.cityTier = cityTier
        this.loyalty = loyalty
        this.specialYear = specialYear
        this.loadedAt = Date.now()
      } catch (e) {
        this.error = e.message || '数据加载失败'
        console.error('Dashboard data load error:', e)
      } finally {
        this.loading = false
      }
    },
  },
})
