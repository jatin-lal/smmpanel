const path = require('path');
const webpack = require('webpack');
var JavaScriptObfuscator = require('webpack-obfuscator');

module.exports = {
   entry: './raws/scripts/main.js',
   output: {
      path: path.join(__dirname, '/dist/js/'),
      filename: 'main.js'
   },
   devServer: {
      inline: true,
      port: 8080
   },
   module: {
      rules: [
      ]
   },
   plugins: [
    new JavaScriptObfuscator ({
      rotateUnicodeArray: true
  })
  ]
}