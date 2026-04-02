import streamlit as st
import requests

st.title('TelcoWeb')
api_url = 'http://127.0.0.1:8000/predict/'


tenure = st.number_input("Срок контракта (tenure)", min_value=0, value=1)
monthly_charges = st.number_input("Месячная оплата", min_value=0.0, value=90.0)
total_charges = st.number_input("Общая оплата", min_value=0.0, value=90.0)
contract_1 = st.selectbox("Контракт на один год", [0, 1])
contract_2 = st.selectbox("Контракт на два года", [0, 1])
fiber = st.selectbox("Оптика Fiber", [0, 1])
no_internet = st.selectbox("Нет интернета", [0, 1])
no_internet_sec = st.selectbox("Нет интернета (безопасность)", [0, 1])
online_sec = st.selectbox("Есть онлайн безопасность", [0, 1])
no_internet_tech = st.selectbox("Нет интернета (техподдержка)", [0, 1])
tech_support = st.selectbox("Есть техподдержка", [0, 1])


if st.button('Проверка'):
    data = {
        "tenure": int(tenure),
        "MonthlyCharges": float(monthly_charges),
        "TotalCharges": float(total_charges),
        "Contract_One_year": int(contract_1),
        "Contract_Two_year": int(contract_2),
        "InternetService_Fiber_optic": int(fiber),
        "InternetService_No": int(no_internet),
        "OnlineSecurity_No_internet_service": int(no_internet_sec),
        "OnlineSecurity_Yes": int(online_sec),
        "TechSupport_No_internet_service": int(no_internet_tech),
        "TechSupport_Yes": int(tech_support)
    }

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 200:
            result = response.json()
            prediction = result['Answer']

            if prediction == 'Churn':
                st.error(f'Результат: {prediction} (Churn No)')
            else:
                st.success(f'Результат: {prediction} (Churn Yes)')
        else:
            st.error(f'Ошибка сервера: {response.status_code}')
            st.write(response.text)

    except requests.exceptions.ConnectionError:
        st.error('Сервер FastAPI не отвечает.')
