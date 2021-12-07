const path = require('path');
const Dotenv = require('dotenv-webpack');

module.exports = {
    module: {
      rules: [
        {
          test: /\.[jt]sx?$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        },
        {
          test: /\.css$/i,
          exclude: /node_modules/,
          use: ["style-loader"],
        },
      ]
    },
    resolve: {
      extensions: [ '.tsx', '.ts', '.js' ],
    },
    output: {
      filename: 'main.js',
      path: path.resolve(__dirname, 'dist', 'js'),
    },
    devtool: 'eval-source-map',
    plugins: [new Dotenv()],
  };