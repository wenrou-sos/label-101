import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'

const babyLight = {
  dark: false,
  colors: {
    background: '#FFF8F3',
    surface: '#FFFFFF',
    'surface-variant': '#FBEFE6',
    primary: '#FF8A65',
    'primary-darken-1': '#E5704F',
    secondary: '#7CB342',
    accent: '#EC9BAE',
    info: '#64B5F6',
    success: '#7CB342',
    warning: '#FFB74D',
    error: '#E57373',
    'on-surface': '#5D4037',
    'on-background': '#5D4037',
  },
  variables: {
    'border-color': '#F0DDD2',
    'border-opacity': 1,
    'medium-emphasis-opacity': 0.78,
    'font-family': "'Noto Sans SC', sans-serif",
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'babyLight',
    themes: { babyLight },
  },
  icons: {
    defaultSet: 'mdi',
  },
  defaults: {
    VCard: {
      rounded: 'xl',
      elevation: 0,
      border: 'thin solid #F0DDD2',
    },
    VBtn: {
      rounded: 'pill',
      style: 'text-transform: none; letter-spacing: 0;',
    },
  },
})
