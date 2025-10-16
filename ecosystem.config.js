module.exports = {
  apps: [
    {
      name: 'aida-flask',
      script: 'app.py',
      interpreter: 'python',
      cwd: './aida-backend',
      env: {
        NODE_ENV: 'development'
      }
    }
  ]
};