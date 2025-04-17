
module.exports = {
    devServer: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8980', // 后端服务地址
          changeOrigin: true, // 是否改变原始主机头为目标URL
        }
      }
    }
  }