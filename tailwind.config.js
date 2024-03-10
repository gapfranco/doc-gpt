/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./core/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  darkMode: 'class',
  plugins: [
      require('@tailwindcss/forms'),
      require('@tailwindcss/typography'),
      require("preline/plugin")
  ],
}
