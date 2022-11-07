/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "mood/templates/mood/*.{html,js}",
    "mood/templates/mood/components/*.{html,js}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {colors: {
      'apple-orange-dark': '#ff9d0a','apple-orange':'#ff9500',
    },},
  },
  plugins: [require('flowbite/plugin')],
}
