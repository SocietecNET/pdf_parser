## BUILD and RUN
`docker build -t pdf-parser .`

then

`docker run -d --restart unless-stopped -p 8000:8000 pdf-parser`
