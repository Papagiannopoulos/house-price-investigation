# Import modules
import pandas as pd
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Find the corresponding path
path = 'Output/Model_in_production'
os.chdir(path)

# Import necessary files for ML production
# Select Features
selected_features = pd.read_excel(f'Selected_features.xlsx').iloc[:,0].tolist()
# Model
xgb = joblib.load(open(f'xgb_model.joblib', 'rb'))

# Import data
data = pd.read_csv('../../Data/test.csv')

# Missing values
quality = {'Ex':5,'Gd': 4,'TA': 3,'Fa': 2,'Po': 1, 'No': 0}
# Pool1QC
data.PoolQC[~data.PoolQC.isna()] = 'Yes'
data.PoolQC.fillna('No', inplace=True)
# MiscFeature
data.MiscFeature[~data.MiscFeature.isna()] = 'Yes'
data.MiscFeature.fillna('No', inplace=True)
# Alley
data.Alley[~data.Alley.isna()] = 'Access'
data.Alley[data.Alley.isna()] = 'No alley access'
# Fence
data.Fence[~data.Fence.isna()] = 'Yes'
data.Fence.fillna('No', inplace=True)
# FireplaceQu
data.FireplaceQu.fillna('No', inplace=True)
# LotFrontage
lotshape_medians = data.groupby("LotShape")["LotFrontage"].median()
data["LotFrontage"] = data["LotFrontage"].fillna(data["LotShape"].map(lotshape_medians))
# GarageQual
data.GarageQual.fillna('No', inplace=True)
# Garage
data.GarageFinish.fillna('No Garage', inplace=True)
data.GarageType.fillna('No Garage', inplace=True)
data.GarageCond.fillna('No', inplace=True)
# Basement
data.BsmtExposure.fillna('No Bsmnt', inplace=True)
data.BsmtFinType2.fillna('No Bsmnt', inplace=True)
data.BsmtFinType1.fillna('No Bsmnt', inplace=True)
data.BsmtCond.fillna('No', inplace=True)
data.BsmtQual.fillna('No', inplace=True)
# MasVnrArea
data.MasVnrArea.fillna(data.MasVnrArea.median(skipna=True), inplace=True)
# Electrical
data.Electrical.fillna(data.Electrical.mode().values[0], inplace = True)

# New features
# Building Age
data['BuildingAge'] = data.YearBuilt.max(skipna=True) - data.YearBuilt + 1
data['Remodeling'] = (data['YearBuilt'] != data['YearRemodAdd'])
# Garage Age
data['GarageYrBlt'] = data.GarageYrBlt.max(skipna=True) - data.GarageYrBlt + 1

# Engineering
# Binary cols
binary_cols = data.apply(lambda x: pd.Series(x).nunique() == 2, axis = 0)
binary_cols = binary_cols[binary_cols].index.tolist()
for col in binary_cols:
    dict_col = {data[col].unique()[0]:0, data[col].unique()[1]:1}
    data[col] = data[col].map(dict_col).astype('boolean')
# Specific cols
data.MSSubClass = data.MSSubClass.astype('O')
data.MoSold = data.MoSold.astype('O')
# Quality related cols
mask = data.columns.str.contains(r'Qu', regex=True)
cols_to_map = data.loc[:, mask].columns.difference(['OverallQual','LowQualFinSF'])
data[cols_to_map] = data[cols_to_map].apply(lambda x: x.map(quality), axis=1)
data.ExterCond = data.ExterCond.map(quality)
data.BsmtCond = data.BsmtCond.map(quality)
data.GarageCond = data.GarageCond.map(quality)
data.HeatingQC = data.HeatingQC.map(quality)

# Selected features
output = pd.DataFrame(data['Id']) # Keep ID
#data = data[selected_features]
#for col in data.select_dtypes(include='O').columns:
#    data[col] = data[col].astype('category')
data = pd.get_dummies(data)
data = data[selected_features]

# Model predictions
output['SalePrice'] = xgb.predict(data)

# Save the output
output.to_csv(f'Sales_list/{pd.Timestamp.now().date()}.csv', index=False)
print(output.head(10))