# 🦠 **House Price Investigation**  
#### 🎯 ***Aim***: Predict the sales price of residential homes in Ames, Iowa

## Project Summary  
This projects focuses into the investigaion of house prices specializing into  
**Data cleaning**, **Feature Selection**, **Hyperparameter Tuning**, **Model development** and **Model production**.  
It is the second most popular competion on Kaggle. Submission file scores at 5% of globe rank.  

## Project Structure  

### Table of Contents  
1. 🔍 **[ Dataset](#-dataset)** - Data source
2. 🧹 **[ Data Cleaning & Engineering](#-data-cleaning-&-engineering)** - Outliers, missing values handling
3. 📊 **[ Feature Selection](#-feature-selection)** - Univariate approaches, correlation elimination, feature importances
4. 👥 **[ Hyperparameter Tuning](#-hyperparameter-tuning)** - Bayesian optimization methods
5. 🧩 **[ Model Development](#-model-development-analysis)** - Extreme Gradient Boosting
6. 🛒 **[ Model Production](#-model-production)** - joblib files for production
7. 🚀 **[ Future Enhancements](#-future-enhancements)** - Next steps and improvements
8. 🔁 **[ Reproducibility](#-reproducibility)** - Install dependencies

## 🔍 Dataset  
I used the Kaggle API (Program > kaggle_data_download.py) to automatically load the dataset.  
Navigate to the [ Reproducibility](#-reproducibility) for more details regarding Kaggle API.  
More info about data is available at the following link.  
- *[📥 Download Source](https://www.kaggle.com/competitions/home-data-for-ml-course)*

## 🧹 Data Cleaning & Engineering  
- **Ordinal features** were encoded according to their natural order, instead of being treated as purely categorical.
- **Categorical features** with low variance or limited predictive value (small RMSE after univariate association with the target) were removed to reduce noise.
- **Missing values** were imputed using business logic relevant to the domain.
- **Outliers** were identified using standardized numerical features.  
A new feature (ColX) was created by computing the mean of all numeric values across each row.  
Observations with ColX values outside the range mean±4×sd were excluded from analysis (~1% removed).
- **Building age** and **garage age** were calculated, along with a **flag for previous house remodeling**.

## 📊 Feature Selection
Two complementary approaches were performed:  
- **Univariate analysis**:  
The relationship between the target and each feature was assessed using linear regression.  
Performance metrics such as Entropy (for categorical features), RMSE, and R² were recorded to guide feature selection.  
- Categorical features with low entropy (less than one-seventh of the maximum possible) were removed.  
- For numerical features, any pair with correlation above a predefined cut-off (0.6) was considered redundant.  
In such cases, the feature with the higher RMSE in the univariate analysis was removed.
- **Multivariate ranking**: A tuned XGBoost model with regularization was trained on the remaining features to assess their importance.  
Features with zero importance were excluded from the final set.  

## 👥 Hyperparameter TuningTwo complementary approaches were performed:
Hyperparameter tuning was performed using **Bayesian optimization** with the **Tree-structured Parzen Estimator (TPE)**, implemented via the treeparzen module.  
Unlike traditional grid/random search, Bayesian optimization constructs a probabilistic surrogate model of the loss function, which it uses to intelligently select the most promising hyperparameter configurations.  
TPE, in particular, models the distribution of “good” versus “bad” hyperparameter configurations and chooses new candidates that maximize the expected improvement based on the given hyperparameter ranges.  

## 🧩 Model Development
Spliting the data into train, test (20%) adn valid (15%), an XGBmodel tuned trained under multiple trials of subjective selections between final features.
Finally, a model with 45 features were selected for production.  

## 🛒 Model Production
- The selected features were saved in an .xlsx file.
- The trained XGBoost model was serialized and stored as a .joblib file for production use.
- The model_in_production.py script implements the prediction procedure, generating an output file containing the ID and the predicted value, with a timestamped filename.

## 🚀 Future Enhancements


## 🔁 Reproducibility
#### 1. Clone repo and cd
git clone https://github.com/Papagiannopoulos/who-covid19-globe-dashboard.git   
cd 'ecommerce-business-analytics'

#### 2. Create a fresh virtual [env](https://github.com/astral-sh/uv)
uv venv  
**Note**: If uv is not already installed, run the following command in PowerShell.  
- On macOS and Linux:  
curl -LsSf https://astral.sh/uv/install.sh | sh  
- On Windows:  
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

#### 3. Sync environment
uv sync  
**Note**: At this step, Microsoft Visual C++ is required. If sync crashes follow the provided steps.

#### 4. Kaggle's API  
1) Create a [Kaggle account](https://www.kaggle.com)  
2) Go to Account Settings and click "Create New API Token" to download the kaggle.json file  
3) Navigate to C:\Users\<your_user_name> on your computer  
4) Create a new folder named .kaggle  
5) Move the downloaded kaggle.json file into the .kaggle folder

#### 5. You are ready!!!
