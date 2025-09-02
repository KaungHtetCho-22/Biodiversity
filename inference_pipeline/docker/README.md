Create .env inside this docker directory with below variables

```txt
AUDIO_DATA_DIR=/home/monsoon/continuous_monitoring_data/live_data # This is where the audio files are coming (@ iNet)
APP_DATA_DIR=${PWD}/app-data/soundscape-model
AUDIO_CLASSIFIER_WEIGHTS=${PWD}/weights/soundscape-model.pt

# Credentials
TOKEN_URL="https://monsoon.co.th/IdentityServer/connect/token"
CLIENT_ID="monsoon-script"
CLIENT_SECRET="secret"
API_USERNAME="console"
API_PASSWORD="M@s00n_2024"
API_URL="https://monsoon.co.th/Server/API/SendIoTDevice"
DATABASE_URL="sqlite:///app-data/soundscape-model.db"
```