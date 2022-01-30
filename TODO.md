# Next steps

## Preprocessing pipeline

This system performs a single preprocessing task on every upload.
We can expect to support:

* larger documents
* greater volumes of documents
* additional preprocessing tasks (lemmatizing, part-of-speech tagging...)

This suggests we move to an asynchronous pipeline, so that preprocessing
does not become a bottleneck.

For very high loads we would require a scaling microservice architecture
where each preprocessing task could be offloaded to a serverless function
(for example, [AWS Lambda](https://aws.amazon.com/lambda/)).

## Decoupled interface

Interface rendering is currently tied to backend processing. If preprocessing
is offloaded (above) or if the user initiates postprocessing tasks, we can
expect to wait for the results.

This suggests using a decoupled JavaScript interface (for example,
[React](https://reactjs.org) or [Ember](https://emberjs.com)) to increase
responsiveness. It may even suggest reducing the backend to an API with
minimal Views (for example,
[Django REST Framework](https://www.django-rest-framework.org) or
[FastAPI](https://fastapi.tiangolo.com)).
