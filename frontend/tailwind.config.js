/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0a0a0a',
          800: '#121212',
          700: '#1a1a1a',
          600: '#2a2a2a',
        },
        accent: {
          blue: '#3b82f6',
          green: '#10b981',
          purple: '#8b5cf6',
        },
      },
    },
  },
  plugins: [],
}
