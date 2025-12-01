/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Dark theme
        background: '#0a0a0a',
        surface: '#1a1a1a',
        border: '#2a2a2a',
        'text-primary': '#e0e0e0',
        'text-secondary': '#a0a0a0',
        'text-tertiary': '#606060',

        // Accents
        accent: '#3b82f6',
        success: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',

        // Emotional states
        'valence-positive': '#10b981',
        'valence-negative': '#ef4444',
        'activation-high': '#f59e0b',
        'certainty-high': '#3b82f6',
        'aperture-open': '#8b5cf6',
        connection: '#ec4899',
      },
    },
  },
  plugins: [],
}
