const colors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: colors.indigo,
        secondary: colors.orange,
      },
    },
  },
  plugins: [],
};
