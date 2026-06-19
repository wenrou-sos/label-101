export const PALETTE = [
  '#FF8A65',
  '#7CB342',
  '#64B5F6',
  '#EC9BAE',
  '#A1887F',
  '#FFB74D',
  '#9575CD',
  '#4DB6AC',
  '#F06292',
  '#7986CB',
  '#AED581',
]

export const COLOR = {
  coral: '#FF8A65',
  mint: '#7CB342',
  sky: '#64B5F6',
  rose: '#EC9BAE',
  brown: '#A1887F',
  amber: '#FFB74D',
  ink: '#4E342E',
  inkSoft: '#6D5546',
  line: '#F0DDD2',
  surface: '#FFFFFF',
  bg: '#FFF8F3',
}

export const PLOT_FONT = {
  family: "'Noto Sans SC', sans-serif",
  size: 12,
  color: '#6D5546',
}

export const PLOT_CONFIG = {
  responsive: true,
  displaylogo: false,
  toImageButtonOptions: {
    format: 'png',
    filename: 'baby-market-chart',
    height: 600,
    width: 1200,
    scale: 2,
  },
  modeBarButtonsToRemove: ['lasso2d', 'select2d'],
}

export function plotLayout(extra = {}) {
  return {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: PLOT_FONT,
    margin: { l: 48, r: 24, t: 30, b: 48 },
    legend: {
      orientation: 'h',
      y: -0.22,
      font: { size: 11, color: '#6D5546' },
    },
    hoverlabel: {
      bgcolor: '#FFFFFF',
      bordercolor: '#F0DDD2',
      font: { color: '#4E342E', family: "'Noto Sans SC', sans-serif" },
    },
    ...extra,
  }
}
