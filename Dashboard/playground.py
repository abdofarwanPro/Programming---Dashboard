import pandas as pd

vaccine_data_frame = pd.read_csv('turkey_vaccine.csv',sep=";")
daily_first_dose_vaccinations = vaccine_data_frame[['daily_first_dose_vaccinations']]

print("Hello")
print("Bye")
