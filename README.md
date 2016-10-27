# @cropsbot

Uses the openface API to find human faces in images from e621.

## How it works

Every so often, the bot downloads a set of images from e621's random pool. You can see what tags it uses in `config.example.yml`.

Since (obviously) there arent' many human faces in images submitted to e621, we have to try an force the shape predictor to find what it thinks is a face. Sometimes it succeeds... otherwise it does not, which is what makes the bot fun. Each *sample* image (e621 stores a scaled ~800px image for each submission) is downloaded, resized and checked against the shape predictor several times; this gives the predictor more chances at finding a face.

If the predictor discovers a match, it will download the source image and scale up the bounding box of the "face" to the full-resolution image. The image is then cropped using a numpy slice and the image is uploaded to @cropsbot. 

# Building for Docker

Installing Openface on any machine requires the installation of hundreds of dependencies for various C++ and Fortran libraries. Instead of going through that pain, we just use Docker instead.   

```
./build.sh
```

# Run with Docker

```
./run.sh
```