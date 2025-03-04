import streamlit as st
from streamlit_javascript import st_javascript

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

from model import ProbaModel

def show(data, n_trim = 6, nxt_trim = 1):
    trim_range = range(nxt_trim, n_trim + 1)

    col_size = [2] * n_trim
    
    right = st.columns(col_size)
    gpa_input = {}
    for trim in trim_range:
        gpa_val = right[trim - 1].number_input(f"GPA of Trim. {trim}",  min_value = 1.00, max_value = 4.00)
        data[f"t{trim}_gpa"] = [gpa_val]
        gpa_input[f"t{trim}_gpa"] = gpa_val

    # for trim in range(1, 7):
    #     gpa = data[f"t{trim}_gpa"].values[0]

    #     st_javascript(f"""localStorage.setItem("student-data-t{trim}_gpa-input", "{gpa}")""")
    
    st_javascript(f"""localStorage.setItem("student-data-trim-gpa-input", "{gpa_input}")""")
    
    model = ProbaModel(start_trim = nxt_trim, phases = ["during"], labels = ["got"])
    _, proba = model.predict(data)
    
    proba_got = [proba["got"][trim][:, 1][0] for trim in trim_range]
    
    test_data = pd.DataFrame()
    for label, proba in zip(["GOT"], [proba_got]):
        current = pd.DataFrame(proba, columns = ["proba"])
        current.insert(0, "trim", trim_range)
        current.insert(1, "label", label)
        test_data = pd.concat([test_data, current])

    fig = px.line(test_data, x = "trim", y = "proba", color = "label")
    fig.update_layout(title = dict(
                    text = "Simulation",
                    font = dict(size=20)
                    ))

    fig.update_xaxes(dtick=1)
    
    st.plotly_chart(fig, use_container_width = True)