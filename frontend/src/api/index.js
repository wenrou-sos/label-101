import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

function buildParams(params = {}) {
  const result = {}
  if (params.start_year !== undefined) result.start_year = params.start_year
  if (params.end_year !== undefined) result.end_year = params.end_year
  return result
}

export async function getOverview(params = {}) {
  const { data } = await http.get('/overview', { params: buildParams(params) })
  return data.data
}

export async function getAgeStageConsumption(params = {}) {
  const { data } = await http.get('/age-stage/consumption', { params: buildParams(params) })
  return data.data
}

export async function getCategoryDecisionFactors(params = {}) {
  const { data } = await http.get('/category/decision-factors', { params: buildParams(params) })
  return data.data
}

export async function getCityTierComparison(params = {}) {
  const { data } = await http.get('/city-tier/comparison', { params: buildParams(params) })
  return data.data
}

export async function getLoyaltySurvival(params = {}) {
  const { data } = await http.get('/loyalty/survival', { params: buildParams(params) })
  return data.data
}

export async function getSpecialYearImpact(params = {}) {
  const { data } = await http.get('/special-year/impact', { params: buildParams(params) })
  return data.data
}
