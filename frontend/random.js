/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src//*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        'neon-green': '#39FF14',
        'neon-pink': '#FF10F0',
        'neon-blue': '#00FFFF',
      }
    },
  },
  plugins: [],
}