import { defineStore } from 'pinia'
import {
  getOverview,
  getAgeStageConsumption,
  getCategoryDecisionFactors,
  getCityTierComparison,
  getLoyaltySurvival,
  getSpecialYearImpact,
} from '../api'
import { ALL_CATEGORIES } from '../constants/charts'

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
    sharedFilter: {
      dimension: 'category',
      value: null,
    },
  }),
  getters: {
    hasActiveFilter: (state) => state.sharedFilter.value !== null,
    activeFilterLabel: (state) => state.sharedFilter.value || '',
    allCategories: () => ALL_CATEGORIES,
  },
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
    setFilter(dimension, value) {
      if (this.sharedFilter.dimension === dimension && this.sharedFilter.value === value) {
        this.clearFilter()
        return
      }
      this.sharedFilter = { dimension, value }
    },
    clearFilter() {
      this.sharedFilter = {
        dimension: 'category',
        value: null,
      }
    },
    isFilteredCategory(categoryName) {
      if (!this.sharedFilter.value) return null
      return this.sharedFilter.value === categoryName
    },
  },
})
