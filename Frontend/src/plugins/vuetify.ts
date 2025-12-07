import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import { md3 } from 'vuetify/blueprints';
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg';

export default createVuetify({
  blueprint: md3,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'tbankTheme',
    themes: {
      tbankTheme: {
        dark: false,
        colors: {
          primary: '#FFD600',
          'on-primary': '#000000',
          secondary: '#212121',
          background: '#F5F5F5',
          surface: '#FFFFFF',
          'surface-variant': '#E0E0E0',
          error: '#D32F2F',
          success: '#388E3C',
        },
        variables: {
          'font-family': 'Manrope, sans-serif',
          'border-radius-root': '12px',
        },
      },
      tbankDarkTheme: {
        dark: true,
        colors: {
          primary: '#FFD600',
          'on-primary': '#000000',
          secondary: '#E0E0E0',
          background: '#121212',
          surface: '#1E1E1E',
          'surface-variant': '#2C2C2C',
          error: '#EF5350',
          success: '#66BB6A',
        },
        variables: {
          'font-family': 'Manrope, sans-serif',
          'border-radius-root': '12px',
        },
      },
    },
  },
  defaults: {
    VBtn: { rounded: 'xl', flat: true, fontWeight: 'bold' },
    VCard: { rounded: 'xl', flat: true },
    VTextField: {
      variant: 'outlined',
      rounded: 'xl',
      density: 'comfortable',
      color: 'primary',
    },
    VAutocomplete: {
      variant: 'outlined',
      rounded: 'xl',
      density: 'comfortable',
      color: 'primary',
    },
    VSelect: {
      variant: 'outlined',
      rounded: 'xl',
      density: 'comfortable',
      color: 'primary',
      menuIcon: 'mdi-chevron-down',
    },
    VSwitch: { color: 'primary', inset: true },
  },
});
