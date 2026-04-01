from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

telco_app = FastAPI()


model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

class SchemaTelco(BaseModel):
    tenure: int
    MonthlyCharges: int
    TotalCharges: int
    Contract_One_year: int
    Contract_Two_year: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int
    TechSupport_No_internet_service: int
    TechSupport_Yes: int

@telco_app.post('/predict/')
async def predict(telco: SchemaTelco):
    telco_dict = telco.model_dump()

    data = [
        telco_dict['tenure'],
        telco_dict['MonthlyCharges'],
        telco_dict['TotalCharges'],
        telco_dict['Contract_One_year'],
        telco_dict['Contract_Two_year'],
        telco_dict['InternetService_Fiber_optic'],
        telco_dict['InternetService_No'],
        telco_dict['OnlineSecurity_No_internet_service'],
        telco_dict['OnlineSecurity_Yes'],
        telco_dict['TechSupport_No_internet_service'],
        telco_dict['TechSupport_Yes']
    ]

    scaled_data = scaler.transform([data])
    pred = model.predict(scaled_data)[0]
    final_pred = 'Churn' if pred == 1 else 'No Churn'
    return {'Answer': final_pred}


if __name__ == "__main__":
    uvicorn.run(telco_app, host="127.0.0.1", port=8000)
