const webpack = require('webpack');
const TerserPlugin = require("terser-webpack-plugin");

let config = {
    entry: [
        './genocrowd/react/src/index.jsx'
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.css$/,
                use: [
                    { loader: 'style-loader' },
                    { loader: 'css-loader' },
                ]
            }
        ]
    },
    output: {
        path: __dirname + '/genocrowd/static/js',
        filename: 'genocrowd.js'
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    optimization: {
      minimize: true,
      minimizer: [new TerserPlugin()],
    },
};

module.exports = config;
