import withMT from "@material-tailwind/html/utils/withMT";
 
/** @type {import('tailwindcss').Config} */
module.exports = withMT({
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        lightGray: "#FAFAFA",
        darkGray: "#E8E8E8",
        darkBlue: "#3938E6",
        borderColor: "#8760FF",
        backgroundColor: "#ecf0f3",
      },
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
});