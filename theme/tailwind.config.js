module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static_src/**/*.js',
    './node_modules/flowbite/**/*.js',  // ← ¡Esto es clave!
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')  // ← Esto activa los componentes
  ],
}