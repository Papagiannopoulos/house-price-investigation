
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(competition_name: str, download_path: str ='.') -> None:
    """
    Download a dataset from Kaggle.

    Parameters:
    - dataset_name: str, dataset identifier in the form 'username/dataset-name'
    - download_path: str, local directory to save the dataset
    """
    api = KaggleApi()
    api.authenticate()
    api.competition_download_files(competition=competition_name, path=download_path)
    print(f"Dataset '{competition_name}' downloaded and extracted to '{download_path}'")