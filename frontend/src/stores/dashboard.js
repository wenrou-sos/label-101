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

export const MIN_YEAR = 2010
export const MAX_YEAR = 2024

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
    yearRange: {
      start: MIN_YEAR,
      end: MAX_YEAR,
    },
    drillDownYear: null,
  }),
  getters: {
    hasActiveFilter: (state) => state.sharedFilter.value !== null,
    activeFilterLabel: (state) => state.sharedFilter.value || '',
    allCategories: () => ALL_CATEGORIES,
    hasYearFilter: (state) =>
      state.yearRange.start !== MIN_YEAR || state.yearRange.end !== MAX_YEAR || state.drillDownYear !== null,
    yearFilterLabel: (state) => {
      if (state.drillDownYear) return `${state.drillDownYear} 年`
      if (state.yearRange.start === state.yearRange.end) return `${state.yearRange.start} 年`
      return `${state.yearRange.start} - ${state.yearRange.end} 年`
    },
    effectiveYearRange: (state) => {
      if (state.drillDownYear) {
        return { start: state.drillDownYear, end: state.drillDownYear }
      }
      return state.yearRange
    },
  },
  actions: {
    async fetchAll(force = false) {
      if (this.loadedAt && !force) return
      this.loading = true
      this.error = null
      try {
        const { start, end } = this.effectiveYearRange
        const params = { start_year: start, end_year: end }
        const [
          overview,
          ageStage,
          decision,
          cityTier,
          loyalty,
          specialYear,
        ] = await Promise.all([
          getOverview(params),
          getAgeStageConsumption(params),
          getCategoryDecisionFactors(params),
          getCityTierComparison(params),
          getLoyaltySurvival(params),
          getSpecialYearImpact(params),
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
    setYearRange(start, end) {
      this.yearRange = { start, end }
      this.drillDownYear = null
      this.loadedAt = null
      return this.fetchAll(true)
    },
    setDrillDownYear(year) {
      if (this.drillDownYear === year) {
        this.clearDrillDown()
        return
      }
      this.drillDownYear = year
      this.loadedAt = null
      return this.fetchAll(true)
    },
    clearDrillDown() {
      this.drillDownYear = null
    },
    clearYearFilter() {
      this.yearRange = { start: MIN_YEAR, end: MAX_YEAR }
      this.drillDownYear = null
      this.loadedAt = null
      return this.fetchAll(true)
    },
    isFilteredCategory(categoryName) {
      if (!this.sharedFilter.value) return null
      return this.sharedFilter.value === categoryName
    },
  },
})
