module.exports = {
  apps: [
    {
      name: "week4-backend",
      script: "../src/index.js",
      env: {
        NODE_ENV: "local",
        PORT: 3000,
        DATABASE_URL: "mongodb://localhost:27017/week4_backend"
      }
    }
  ]
};
