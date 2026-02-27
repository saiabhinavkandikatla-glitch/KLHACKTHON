# Healthcare Fraud Detection Pipeline

A clean, modular data pipeline designed for quick integration in healthcare fraud detection tasks, specifically optimized for Kaggle healthcare fraud datasets.

## Features

- **Modular Architecture**: Separate modules for data loading, preprocessing, and orchestration.
- **Robust Loading**: Includes file existence checks and error handling.
- **Automated Cleaning**:
    - **Duplicate Removal**: Automatically drops redundant rows.
    - **Intelligent Imputation**: Fills missing numeric values with the median and categorical values with the mode.
    - **Date Normalization**: Automatically detects and converts date-like columns to standard datetime format.
- **ML Integration**:
    - **Feature Separation**: Splits data into features `X` and target label `y` (`PotentialFraud`).
    - **ID Filtering**: Drops high-cardinality ID columns (e.g., ClaimID, Provider, Physician IDs) from ML input while retaining them for output.
    - **Numeric Scaling Entry**: Automatically filters for numeric columns. In the real Kaggle dataset, these typically include:
        - `InscClaimAmtReimbursed`
        - `DeductibleAmtPaid`
        - `ClmProcedureCode_1` through `ClmProcedureCode_6`
- **Real Data Support**: Optimized to merge feature files (Inpatient/Outpatient) with provider-level labels.

## Project Structure

- `Dataset/`: Folder containing the real Kaggle healthcare fraud CSV files.
- `data_loader.py`: Handles CSV loading and merging (e.g., merging features and labels on `Provider`).
- `preprocessing.py`: Contains data cleaning logic (duplicates, nulls, date conversion, feature filtering).
- `main_pipeline.py`: Orchestrates the end-to-end flow with support for real datasets.
- `requirements.txt`: List of necessary Python dependencies.

## Setup

1. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the pipeline by passing the path to your features CSV and optionally the labels CSV:

```bash
python main_pipeline.py --file Dataset/Train_Inpatientdata-1542865627584.csv --labels Dataset/Train-1542865627584.csv
```

The script will:
1. Load and validate the data.
2. Remove duplicate rows.
3. Impute missing values (median for numeric, mode for categorical).
4. Convert date-like columns to datetime objects.
5. Save the cleaned dataset to `cleaned_claims.csv`.
6. Output a feature set `X` (numeric only) and label `y` (PotentialFraud) ready for ML models.

## Verification

You can verify the pipeline by running it with the real dataset:

```bash
python main_pipeline.py --file Dataset/Train_Inpatientdata-1542865627584.csv --labels Dataset/Train-1542865627584.csv
```

## Running the Dashboard

To run the full application (Backend + Frontend), you need two terminal windows:

### 1. Start the Backend (FastAPI)

Navigate to the `backend` directory and start the Uvicorn server:

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --port 8000 --reload
```
*The API will be available at `http://localhost:8000/dashboard`*

### 2. Start the Frontend (React + Vite)

Open a new terminal, navigate to the `arogya-vigilant` directory, and start the development server:

```bash
cd arogya-vigilant
npm install
npm run dev
```
*The dashboard will be available at `http://localhost:5173`*
