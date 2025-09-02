# Biodiversity

This repository contains all source code, instructions, and services required for the complete technical documentation.  

The project is divided into three main components, each with its own documentation and setup guide:  

---

## 0. Custom pi-setup 

This module covers how the raspberry pi is setup for recording and transferring the audio files to iNET via FTPS. Flashed image is uploaded to this google drive link as well **[Download Raspberry Pi OS Image](https://drive.google.com/drive/folders/19RC69tCjV7lfupJODWT0BL_QIx_DtFqr)**

## 1. Audio Classification Training  

This module covers the training of bird and insect sound classification model.  
- See the `README.md` file in this directory for:  
  - Docker setup  
  - Training instructions  

---

## 2. Score Prediction Training  

This module focuses on training the bio-scoring system based on species counts.  
- See the `README.md` file in this directory for:  
  - Environment setup  
  - Training process  
  - Explanation of the scoring logic  

---

## 3. Inference Pipeline  

This is the core pipeline that connects all processes together.  


<!-- 2. **Inference** – Receive audio files from the iot-devices, run inference using the sound classification model, and store the results (predicted species) in an SQLite database.  
3. **Scoring** – Fetch the predictions from the database and apply the score prediction model to calculate the daily biodiversity score based on species counts.   -->

- See the `README.md` file in this directory for:  
  - Environment setup  
  - Workflow logic

---

**[Documenation](https://KaungHtetCho-22.github.io/mkdocs-bio/)**