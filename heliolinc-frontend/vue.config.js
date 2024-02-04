const path = require('path');
const webpack = require('webpack');
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
    // Proxy settings for the dev server
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8332',
                changeOrigin: true,
            },
        },
    },
    transpileDependencies: true,
    configureWebpack: {
        plugins: [
            // Ignore node_modules so they're not watched
            new webpack.WatchIgnorePlugin({
                paths: [path.join(__dirname, 'node_modules')]
            }),
        ]
    }
});
