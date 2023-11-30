const colors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: colors.emerald,
        secondary: colors.indigo,
      },
    },
  },
  plugins: [],
};
