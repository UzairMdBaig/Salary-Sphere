import streamlit as st
import pickle
import numpy as np

countries = ("United States of America",
"Germany",
"United Kingdom of Great Britain and Northern Ireland",
"Canada",
"India",
"France",
"Netherlands",
"Australia",
"Brazil",
"Spain",
"Sweden",
"Italy",
"Poland",
"Switzerland",
"Denmark",
"Norway"
)

dev_types = (
"Developer, full-stack",
"Developer, back-end",
"Developer, front-end",
"Developer, desktop or enterprise applications",
"Engineering manager",
"Developer, embedded applications or devices",
"Developer, mobile",
"Data scientist or machine learning specialist",
"DevOps specialist",
"Engineer, data",
"Cloud infrastructure engineer",
"Data or business analyst"
)

education_level = (
"Bachelor’s degree (B.A., B.S., B.Eng., etc.)",
"Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",
"Less than Batchelor's degree",
"Professional degree (JD, MD, Ph.D, Ed.D, etc.)"
)

job_types = (
"hybrid (some remote, some in-person)",
"In-person",
"Remote"
)

def load_model():
    with open('model_and_more.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data["model"]
country_enc = data["country_encoder"]
devtype_enc = data["dev_encoder"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict your salary""")

    country = st.selectbox("country",countries)
    dev_type = st.selectbox("speciality",dev_types)
    col1, col2 = st.columns(2)
    with col1:
        education = st.radio("Level of Education",education_level)
    with col2:
        job_type = st.radio("Job type",job_types)

    experience = st.slider("Experience in years",0,50,3)
    ok = st.button("Calcuate Salary")
    if ok:
        x = np.array([[country,dev_type,experience]])

        x[:,0] = country_enc.transform(x[:,0])
        x[:,1] = devtype_enc.transform(x[:,1])

        for i in education_level:
            if education == i:
                x = np.append(x,1).reshape(1,-1)
            else:
                x = np.append(x,0).reshape(1,-1)

        for i in job_types:
            if job_type == i:
                x = np.append(x,1).reshape(1,-1)
            else:
                x = np.append(x,0).reshape(1,-1)
        x = x.astype(float)
        salary = model.predict(x)
        salary = np.round(salary,0).astype(int)[0]
        st.subheader(f"The estimated salary is ${salary}")
