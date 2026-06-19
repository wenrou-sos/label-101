import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export async function getOverview() {
  const { data } = await http.get('/overview')
  return data.data
}

export async function getAgeStageConsumption() {
  const { data } = await http.get('/age-stage/consumption')
  return data.data
}

export async function getCategoryDecisionFactors() {
  const { data } = await http.get('/category/decision-factors')
  return data.data
}

export async function getCityTierComparison() {
  const { data } = await http.get('/city-tier/comparison')
  return data.data
}

export async function getLoyaltySurvival() {
  const { data } = await http.get('/loyalty/survival')
  return data.data
}

export async function getSpecialYearImpact() {
  const { data } = await http.get('/special-year/impact')
  return data.data
}
