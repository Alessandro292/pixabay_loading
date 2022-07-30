### Project introduction

The aim of this project is to download, save and make an aggregation count of the source images

As a pictures source I used [Pixabay](https://pixabay.com/)

The app is built with FastAPI Framework Python

Minio is used as blob storage. Images and their metadata are stored using Python Minio Client

MYSql is used as database for storing images metadata

### How to use

In order to get a series of images from this source, we need to get the api key of Pixabay.
Therefore, we should sign in Pixabay (with a google mail) and copying the api key from the link [Pixabay-Developer](https://pixabay.com/api/docs/).

Then is necessary open your docker-compose.yaml e and writing your key as a env var
`PIXABAY_API_KEY: <YOUR_API_KEY>`
If you want start the application not from docker-compose, edit the script ./app/src/config/variables.py
`PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '<YOUR_API_KEY>')`
Replace *** with you api key

We are ready for launching our application.

`docker compose up`

Browsing in [localhost:8000/docs](localhost:8000/docs) for viewing the swagger

Select the endpoint /pixabay/download
Push the bottom 'try it out' and the 'execute'
We can pass some parameters such as animals and languages in order to filter images from Pixabay.

Images and metadata json are stored in Minio and the output in console from the endpoint /pixabay/count is something like this

`{
  "count_animal": [
    {
      "cats": 62
    },
    {
      "birds": 10
    }
  ]
}`

Metadata json looks like 

`{"Filename": "cat-7305013_150.jpg", "cats", "it", "Image Height": 150, "Image Width": 100, "Image Format": "JPEG", "Image Mode": "RGB", "Image is Animated": false, "Frames in Image": 1}`
