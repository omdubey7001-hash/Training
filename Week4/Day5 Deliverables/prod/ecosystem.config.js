module.exports = {
  apps: [
    {
      name: "week4-backend",
      script: "../src/index.js",
      instances: "max",
      exec_mode: "cluster",
      env: {
        NODE_ENV: "production",
        PORT: 3000
      }
    }
  ]
};
