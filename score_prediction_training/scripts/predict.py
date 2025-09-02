import joblib
import pandas as pd

# Load the saved model
loaded_model = joblib.load('results/weights/best_xgboost_model_70_1.0000_f1_1.0000.pkl')
print("Model loaded successfully.")
selected_features = ['hour', 'Abroscopus-superciliaris', 'Acheta-domesticus',
       'Alcedo-atthis', 'Alophoixus-pallidus', 'Anthus-hodgsoni',
       'Cacomantis-merulinus', 'Cacomantis-sonneratii',
       'Centropus-bengalensis', 'Centropus-sinensis', 'Ceryle-rudis',
       'Chrysocolaptes-guttacristatus', 'Conocephalus-fuscus',
       'Culicicapa-ceylonensis', 'Cyornis-whitei', 'Dicrurus-leucophaeus',
       'Dicrurus-remifer', 'Erpornis-zantholeuca', 'Eudynamys-scolopaceus',
       'Eumodicogryllus-bordigalensis', 'Eurystomus-orientalis',
       'Galangal-abeculata', 'Gallus-gallus', 'Glaucidium-cuculoides',
       'Gryllus-bimaculatus', 'Halcyon-smyrnensis',
       'Harpactes-erythrocephalus', 'Hierococcyx-sparverioides',
       'Hirundo-rustica', 'Human_noise', 'Human_vocal', 'Hypothymis-azurea',
       'Hypsipetes-leucocephalus', 'Ixos-mcclellandii', 'Mechanical',
       'Merops-leschenaulti', 'Merops-orientalis', 'MotorvehicleEngine',
       'Myiomela-leucura', 'Noise', 'Oecanthus-pellucens', 'Parus-minor',
       'Pericrocotus-speciosus', 'Phaenicophaeus-tristis',
       'Phaneroptera-falcata', 'Phaneroptera-nana', 'Phoenicurus-auroreus',
       'Phyllergates-cucullatus', 'Phylloscopus-humei',
       'Phylloscopus-tephrocephalus', 'Picumnus-innominatus', 'Plane',
       'Platypleura-sp13', 'Psilopogon-asiaticus', 'Psilopogon-haemacephalus',
       'Psilopogon-lineatus', 'Psilopogon-virens', 'Pycnonotus-aurigaster',
       'Ruspolia-nitidula', 'Saxicola-stejnegeri', 'Siren',
       'Spilopelia-chinensis', 'Surniculus-lugubris', 'Thunderstorm', 'Train',
       'Turnix-suscitator', 'Turnix-tanki', 'Upupa-epops',
       'Urosphena-squameiceps', 'Yungipicus-canicapillus']

# print(len(selected_features))

df = pd.read_csv("forestia_processed_df.csv")  # Replace with actual file

df['Conocephalus-fuscus'] = 0
df['Gryllus-bimaculatus'] = 0
df['Merops-orientalis'] = 0
df['Phaneroptera-nana'] = 0
df['Platypleura-sp13'] = 0
# df['Platypleura-plumosa'] = 0 
df['Turnix-tanki'] = 0
df['Acheta-domesticus'] = 0
# df['Chrysococcyx-maculatus'] = 0 
# df['Copsychus-malabaricus'] = 0 
# df['Platypleura-cfcatenata'] = 0
# df['Platypleura-sp12cfhirtipennis'] = 0
# df['Phaneroptera-nana'] = 0
df['Ruspolia-nitidula'] = 0
# df['Spilopelia-chinensis'] = 0
df['Oecanthus-pellucens'] = 0
df['Phaneroptera-falcata'] = 0

new_data = df[selected_features]  # Select only relevant features

# Make predictions
new_predictions = loaded_model.predict(new_data)
new_predictions = new_predictions.copy()

predictions = df[['unique_date']].copy()
predictions['device_area'] = predictions['unique_date'].apply(lambda x: '_'.join(x.split('_')[:1]))
predictions.drop('unique_date', axis=1, inplace=True)
predictions['score_prediction'] = pd.Series(new_predictions)

class_counts = predictions.groupby('device_area')['score_prediction'].value_counts().unstack(fill_value=0)

# Add a "Total" column summing all class counts for each device area
sum = class_counts.sum(axis=1)

scores = {0: 'A', 1:'B', 2:'C'}
# Print results
pred_percent = []
for device, counts in class_counts.iterrows():
    print(f"Device Area: {device}")
    for score, count in counts.items():
        pred_percent.append(count/sum[device]*100)
        print(f"  Class {scores[score]}: {count}, Votes: {(count/sum[device])*100:.2f}%")
    # print(f"  Total: {counts['Total']}")
    print("-" * 30)  # Separator for readability

### Arbitrarily setting the thresholds for each class:
### In this setting, the prediction accounts in a sequence
### 1. Predicts class "B", if the contribution for class "B" is more than 13%.
### 2. Predicts class "A", if No.1 threshold is not matched and the contribution for class "A" is more than 6%.
### 3. Predicts class "C", if both No.1 and No.2 criteria are not matched.
if pred_percent[1] > 13:
    final_prediction = "B"
elif pred_percent[0] > 6:
    final_prediction = "A"
else:
    final_prediction = "C"

print("########## Final Prediction ##########")
print("Biodiversity Score Level: ", final_prediction)
print("##########")
predictions.to_csv('bioscore_predictions.csv', index=False)
