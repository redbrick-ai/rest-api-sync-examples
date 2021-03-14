# RedBrick AI Custom brick integration

The purpose of this Repository is to give examples of how you write your own "brick" to interface with
a RedBrick AI Pipeline.

The examples here are for a "synchronous" invocation. This means that the output of the brick must returned in the response.

For the ability to process tasks asynchronously, you can use the remote-labeling brick.

# How to use this repository

Create a fork and use the examples as a starting point.

Your code can run anywhere, as long as the RedBrick AI application can access the API endpoint, it does not matter where or how your code is hosted.

The examples here are built in Python Flask but you can build your own in any language.

If you already have an account on Amazon Web Services (AWS) then we recommend using API Gateway + Lambda as a serverless solution to easily handle the potentially
sporadic requests to your custom brick.

## Example 1: Converting bounding boxes into polygons

This is a slightly trivial use case that manipulates bounding box labels into polygons

The pipeline configuration for a stage would look like this:

```json
{
  "stageName": "<stageName>",
  "brickName": "rest-api-sync",
  "routing": {
    "stageNames": ["<nextStage>"]
  },
  "stageConfig": {
    "apiEndpoint": "<api to be called>"
  },
  "inputType": "IMAGE_BBOX",
  "outputType": "IMAGE_POLYGON",
  "inputTaxonomyName": "<taxonomy>",
  "inputTaxonomyVersion": "<taxonomyVersion>",
  "outputTaxonomyName": "<taxonomy>",
  "outputTaxonomyVersion": "<taxonomyVersion>"
}
```
