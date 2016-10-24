# Building for Docker

```
docker build --tag fisk:lewdcrops
```

# Run

```
docker run -v /Users/fiskie/docker/lewdcrops/src:/root/lewdcrops -p 9000:9000 -p 8000:8000 -t fisk:lewdcrops -d
```