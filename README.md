## BUILD and RUN
`docker build -t pdf-parser .`

### Running with API Key
For development/testing:
```bash
docker run -d --restart unless-stopped -p 8000:8000 -e API_KEY=your-secret-key pdf-parser
```

For production (recommended):
1. Create a `.env` file:
```bash
echo "API_KEY=your-production-secret-key" > .env
```
2. Run with:
```bash
docker run -d --restart unless-stopped -p 8000:8000 --env-file .env pdf-parser
```

> Important: Replace `your-secret-key` with a strong, random string and keep it secure.
