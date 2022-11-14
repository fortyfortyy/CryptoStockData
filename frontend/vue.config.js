module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? '/static/dist/' : 'http://localhost:8080',
    outputDir: '../backend/static/dist',
    indexPath: '../../templates/base-vue.html', // relative to outputDir!
    filenameHashing: false, // Django will hash file names, not webpack
    runtimeCompiler: true,
    devServer: {
        devMiddleware: {
            // see https://github.com/webpack/webpack-dev-server/issues/2958
            writeToDisk: true,
        }
    },
}