# app.py
import json

from flask import Flask, request
from marshmallow import Schema, fields

app = Flask(__name__)


class AttributeSchema(Schema):
    name = fields.String(required=True)
    value = fields.Raw(required=True)


class Bbox2dSchema(Schema):
    xnorm = fields.Float(required=True)
    ynorm = fields.Float(required=True)
    wnorm = fields.Float(required=True)
    hnorm = fields.Float(required=True)


class PointDataSchema(Schema):
    xnorm = fields.Float(required=True)
    ynorm = fields.Float(required=True)


class LabelSchema(Schema):
    category = fields.List(
        fields.List(fields.String(required=True), required=True), required=True
    )
    attributes = fields.List(fields.Nested(AttributeSchema), required=True)

    bbox2d = fields.Nested(Bbox2dSchema)
    point = fields.Nested(PointDataSchema)
    polyline = fields.List(fields.Nested(PointDataSchema))
    polygon = fields.List(fields.Nested(PointDataSchema))
    # Note: incomplete


class RequestSchema(Schema):
    org_id = fields.UUID(required=True)
    project_id = fields.UUID(required=True)
    stage_name = fields.String(required=True)
    task_id = fields.UUID(required=True)
    dp_id = fields.UUID(required=True)
    items = fields.List(fields.String(required=True), required=True)
    items_presigned = fields.List(fields.String(required=True), required=True)
    input_type = fields.String(required=True)
    expected_type = fields.String(required=True)
    expected_taxonomy_name = fields.String(required=True)
    expected_taxonomy_version = fields.Integer(required=True)
    downstream_stages = fields.List(fields.String(required=True), required=True)

    labels = fields.List(fields.Nested(LabelSchema))
    labeled_by_user_id = fields.UUID()
    labeled_by_email = fields.String()


class ResponseSchema(Schema):
    labels = fields.List(fields.Nested(LabelSchema))
    routing_code = fields.Integer()
    custom_sub_name = fields.String()
    status_code = fields.Integer(required=True)


@app.route("/")
def hello():
    return "Hello World!"


@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/example1", methods=["POST"])
def example1():

    input_data = request.data.decode("utf-8")
    input_data = json.loads(input_data)
    print(input_data)
    assert input_data.get("input_type") == "IMAGE_BBOX"
    assert input_data.get("expected_type") == "IMAGE_POLYGON"

    labels = input_data.get("labels")

    labels_output = []
    for label in labels:
        xnorm = label["bbox2d"]["xnorm"]
        ynorm = label["bbox2d"]["ynorm"]
        hnorm = label["bbox2d"]["hnorm"]
        wnorm = label["bbox2d"]["wnorm"]

        new_label = {
            "category": label["category"],
            "attributes": label["attributes"],
            "polygon": [
                {"xnorm": xnorm, "ynorm": ynorm},
                {"xnorm": xnorm + wnorm, "ynorm": ynorm},
                {"xnorm": xnorm + wnorm, "ynorm": ynorm + hnorm},
                {"xnorm": xnorm, "ynorm": ynorm + hnorm},
            ],
        }
        labels_output.append(new_label)
    return {"labels": labels_output, "status_code": 200}


@app.route("/example2", methods=["POST"])
def example2():

    input_data = request.data.decode("utf-8")
    input_data = json.loads(input_data)
    print(input_data)
    assert input_data.get("input_type") == "IMAGE_BBOX"
    assert input_data.get("expected_type") == "IMAGE_BBOX"

    labels = input_data.get("labels")

    # filter out small boxes
    labels = list(
        filter(
            lambda x: x["bbox2d"]["wnorm"] > 0.001 and x["bbox2d"]["hnorm"] > 0.001,
            labels,
        )
    )

    unique_categories = set()

    for label in labels:
        unique_categories.add(label["category"][0][1])

    #
    routing_code = 0
    if len(unique_categories) < 5:
        routing_code = 1

    return {
        "labels": labels,
        "status_code": 200,
        "routing_code": routing_code,
        "custom_sub_name": "Min_bbox_size",
    }
