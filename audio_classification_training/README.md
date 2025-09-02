# Biodiversity Audio Classification

Biodiversity Audio Classification repository. This project is dedicated to training machine learning models to classify audio recordings of wildlife, with a specific focus on bird species from Chiang Mai, Thailand. It is possible to classify more bird species or other animals based on their sounds as heard in their natural habitat. 

The codebase is adapted from [BirdCLEF 2023 4th Place Solution](https://www.kaggle.com/competitions/birdclef-2023/discussion/412753). We train without knowledge distillation and only for a single fold for simplicity. 

## Quick Start with Docker

We provide a Docker environment that encapsulates all necessary dependencies. 

To build the container and start running the container
- ```cd audio_classification_training```
- ```sh docker/build_docker.sh```
- ```sh docker/run_docker.sh```

After setting up the docker environments, follow the detailed instructions in the [`train`](./train/) folder.

## Dataset

To train models with the provided code: We will upload the sound files that is used at here later cause the file size is too big.

## Machine used to train the model 

- GPU: NVIDIA GeForce RTX 4090 - 24GB VRAM
- CPU: Intel(R) Core(TM) i9-14900F
- RAM: 64 GB





