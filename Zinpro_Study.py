


# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:59:31 2024

@author: marco
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
#from numerize.numerize import numerize
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title='Zinpro', page_icon='Zinpro', layout='wide')
# Custom CSS for the header color
st.markdown(
    """
    <style>
    .header {
        color: #00009e;
        font-size: 4em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom CSS class for the header
st.markdown('<h1 class="header">Zinc and chrome study</h1>', unsafe_allow_html=True)

# Custom CSS for the subheader color
st.markdown(
    """
    <style>
    .subheader {
        color: #00000;
        font-size: 1.5em; /* Adjust the size to make it appropriate for a subheader */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom CSS class for the subheader
st.markdown('<h2 class="subheader">Effects of Isoferm inclusion in Broilers diets</h2>', unsafe_allow_html=True)


#st.subheader('Effects of Isoferm inclusion in Broilers diets')
st.markdown('------------')
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom CSS class to center the subheader
st.markdown('<h2 class="center-text">Performance by Age</h2>', unsafe_allow_html=True)

#########



# Load the data from an Excel file
df = pd.read_excel("sergio_study.xlsx", sheet_name='Age', na_values='NaN')
df['BWG'] = df["BWG"] / 1000
df2 = pd.read_excel("sergio_study.xlsx", sheet_name='P')


# Display sidebar image
st.sidebar.image("Zinpro.png", caption='Zinpro Availa')

# Sidebar for selecting age
st.sidebar.header('Select Age')
age = st.sidebar.selectbox('Select Age', df['Age'].unique())

# Filter the dataframe based on selected age
age_filtered = df[df['Age'] == age]

# Map treatment codes to names
age_filtered['TR'] = age_filtered['TR'].map({1: 'IM', 2: 'Availa-iso', 3: 'Availa-high'})

# Aggregate the data to get the mean for each treatment
aggregated_data = age_filtered.groupby('TR', as_index=False).mean().round(3)

# Drop the 'Age' column from the aggregated data
aggregated_data_no_age = aggregated_data.drop(columns=['Age'])

# Display the mean values grouped by treatment
st.write("Average Values by Treatment")
st.dataframe(aggregated_data_no_age)


# Define the color map
color_map = {'IM': '#000000', 'Availa-iso': '#000061', 'Availa-high': '#00009e'}

# Create columns for the plots
col1, col2 = st.columns(2)
col3, = st.columns(1)

# Plot Body Weight Gain (BWG) using Plotly
y = 'BWG'
age_p = df2[df2['Age'] == age].loc[:, y].round(3)
error_y = age_filtered.groupby('TR')[y].std()

fig_bwg = px.bar(aggregated_data_no_age, x='TR', y=y, title='Body Weight Gain (BWG)',
                 color='TR', color_discrete_map=color_map,
                 category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                 error_y=error_y)

fig_bwg.update_layout(
    template="plotly_white",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,  # Hide horizontal grid lines
        range=[age_filtered[y].min() * 0.9, age_filtered[y].max() + age_filtered[y].std()]  # Set the range of the Y-axis
    )
)

p_value_bw = age_p.iloc[0]
annotation_text = "<i>P</i> < 0.001" if p_value_bw < 0.001 else f"<i>P</i> = {p_value_bw}"

fig_bwg.add_annotation(
    text=annotation_text,
    xref="paper", yref="paper",
    x=1, y=1.05,  # Position it in the upper right corner
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

# Define letter annotations based on age
letters = []
if age == 21:
    letters = ['a', 'b', 'b']
elif age == 34:
    letters = ['b', 'b', 'a']

# Add letter annotations to the BWG chart
for i, letter in enumerate(letters):
    fig_bwg.add_annotation(
        text=letter,
        x=aggregated_data_no_age['TR'][i],
        y=aggregated_data_no_age[y][i] + error_y.iloc[i] * 1.8,  # Position above the error bar
        showarrow=False,
        font=dict(
            size=14,
            color="black"
        ),
        align="center"
    )

col1.plotly_chart(fig_bwg)

# Plot Feed Intake (FI) using Plotly
y = 'FI'
age_p = df2[df2['Age'] == age].loc[:, y].round(3)
error_y = age_filtered.groupby('TR')[y].std()

fig_FI = px.bar(aggregated_data_no_age, x='TR', y=y, title='Feed Intake (FI)',
                color='TR', color_discrete_map=color_map,
                category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                error_y=error_y)

fig_FI.update_layout(
    template="plotly_white",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,  # Hide horizontal grid lines
        range=[age_filtered[y].min() * 0.9, age_filtered[y].max() + age_filtered[y].std()]  # Set the range of the Y-axis
    )
)

p_value_fi = age_p.iloc[0]
annotation_text = "<i>P</i> < 0.001" if p_value_fi < 0.001 else f"<i>P</i> = {p_value_fi}"

fig_FI.add_annotation(
    text=annotation_text,
    xref="paper", yref="paper",
    x=1, y=1.05,  # Position it in the upper right corner
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

col2.plotly_chart(fig_FI)

# Plot Feed Conversion Ratio (FCR) using Plotly
y = 'FCR'
error_y = age_filtered.groupby('TR')[y].std()
age_p = df2[df2['Age'] == age].loc[:, y].round(3)

fig_FCR = px.bar(aggregated_data_no_age, x='TR', y=y, title='Feed Conversion Ratio (FCR)',
                 color='TR', color_discrete_map=color_map,
                 category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                 error_y=error_y)

fig_FCR.update_layout(
    template="plotly_white",
    plot_bgcolor="white",
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,  # Hide horizontal grid lines
        range=[age_filtered[y].min() * 0.9, age_filtered[y].max() + age_filtered[y].std()]  # Set the range of the Y-axis
    )
)

fig_FCR.add_annotation(
    text=f"<i>P</i> = {age_p.iloc[0]}",
    xref="paper", yref="paper",
    x=1, y=1.05,  # Position it in the upper right corner
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

# Define letter annotations based on age
letters = []
if age == 21:
    letters = ['a', 'b', 'b']
elif age == 34:
    letters = ['a', 'b', 'b']

# Add letter annotations to the BWG chart
for i, letter in enumerate(letters):
    fig_FCR.add_annotation(
        text=letter,
        x=aggregated_data_no_age['TR'][i],
        y=aggregated_data_no_age[y][i] + error_y.iloc[i] * 1.8,  # Position above the error bar
        showarrow=False,
        font=dict(
            size=14,
            color="black"
        ),
        align="center"
    )

col3.plotly_chart(fig_FCR)

st.markdown('------------')

##############################################
# cumulative
df3 = pd.read_excel("sergio_study.xlsx", sheet_name='Cumulative', na_values='NaN')
df4 = pd.read_excel("sergio_study.xlsx", sheet_name='P_cumulative', na_values='NaN')

#st.subheader('Cumulative Age')
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom CSS class to center the subheader
st.markdown('<h2 class="center-text">Performance by cumulative Age</h2>', unsafe_allow_html=True)

# Select cumulative age
st.sidebar.header('Select Cumulative Age')
age_cum = st.sidebar.selectbox('Select Cumulative Age', df3['Age'].unique())

# Filter the dataframe based on selected cumulative age
age_filtered_cum = df3[df3['Age'] == age_cum]

# Map treatment codes to names
age_filtered_cum['TR'] = age_filtered_cum['TR'].map({1: 'IM', 2: 'Availa-iso', 3: 'Availa-high'})

# Aggregate the data to get the mean for each treatment
aggregated_data_cum = age_filtered_cum.groupby('TR', as_index=False).mean().round(3)

# Drop the 'Age' column from the aggregated data
aggregated_data_no_age_cum = aggregated_data_cum.drop(columns=['Age'])

# Display the mean values grouped by treatment
st.write("Average Values by Treatment")
st.dataframe(aggregated_data_no_age_cum)

######charts

# Plot Body Weight Gain (BWG) using Plotly
col6, col7 = st.columns(2)
col8, col9 = st.columns(2)


y = 'BWG'
age_p_cum = df4[df4['Age'] == age_cum].loc[:, y].round(3)
error_y_cum = age_filtered_cum.groupby('TR')[y].std()

fig_bwg_cum = px.bar(aggregated_data_no_age_cum, x='TR', y=y, title='Body Weight Gain (BWG)',
                 color='TR', color_discrete_map=color_map,
                 category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                 error_y=error_y_cum)

fig_bwg_cum.update_layout(
    template="plotly_white",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,  # Hide horizontal grid lines
        range=[age_filtered_cum[y].min() * 0.9, age_filtered_cum[y].max() + age_filtered_cum[y].std()]  # Set the range of the Y-axis
    )
)

fig_bwg_cum.add_annotation(
    text=f"<i>P</i> = {age_p_cum.iloc[0]}",
    xref="paper", yref="paper",
    x=1, y=1.05,  # Position it in the upper right corner
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

# Define letter annotations based on age
letters_cum = []
if age_cum == 21:
    letters_cum = ['a', 'b', 'b']


# Add letter annotations to the BWG chart
for i, letter_cum in enumerate(letters_cum):
    fig_bwg_cum.add_annotation(
        text=letter_cum,
        x=aggregated_data_no_age_cum['TR'][i],
        y=aggregated_data_no_age_cum[y][i] + error_y_cum.iloc[i] * 1.8,  # Position above the error bar
        showarrow=False,
        font=dict(
            size=14,
            color="black"
        ),
        align="center"
    )

col6.plotly_chart(fig_bwg_cum)

y = 'FI'
age_p_cum = df4[df4['Age'] == age_cum].loc[:, y].round(3)
error_y_cum = age_filtered_cum.groupby('TR')[y].std()

fig_FI_cum = px.bar(aggregated_data_no_age_cum, x='TR', y=y, title='Feed Intake',
                 color='TR', color_discrete_map=color_map,
                 category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                 error_y=error_y_cum)

fig_FI_cum.update_layout(
    template="plotly_white",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,  # Hide horizontal grid lines
        range=[age_filtered_cum[y].min() * 0.9, age_filtered_cum[y].max() + age_filtered_cum[y].std()]  # Set the range of the Y-axis
    )
)

fig_FI_cum.add_annotation(
    text=f"<i>P</i> = {age_p_cum.iloc[0]}",
    xref="paper", yref="paper",
    x=1, y=1.05,  # Position it in the upper right corner
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

# Define letter annotations based on age
letters_cum = []
if age_cum == 21:
    letters_cum = ['a', 'b', 'b']


# Add letter annotations to the BWG chart
for i, letter_cum in enumerate(letters_cum):
    fig_FI_cum.add_annotation(
        text=letter_cum,
        x=aggregated_data_no_age_cum['TR'][i],
        y=aggregated_data_no_age_cum[y][i] + error_y_cum.iloc[i] * 1.8,  # Position above the error bar
        showarrow=False,
        font=dict(
            size=14,
            color="black"
        ),
        align="center"
    )

col7.plotly_chart(fig_FI_cum)

y = 'FCR'
age_p_cum = df4[df4['Age'] == age_cum].loc[:, y].round(3)
error_y_cum = age_filtered_cum.groupby('TR')[y].std()

fig_FCR_cum = px.bar(aggregated_data_no_age_cum, x='TR', y=y, title='Feed Conversion Ratio',
                 color='TR', color_discrete_map=color_map,
                 category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                 error_y=error_y_cum)

fig_FCR_cum.update_layout(
    template="plotly_white",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,  # Hide horizontal grid lines
        range=[age_filtered_cum[y].min() * 0.9, age_filtered_cum[y].max() + age_filtered_cum[y].std()]  # Set the range of the Y-axis
    )
)

fig_FCR_cum.add_annotation(
    text=f"<i>P</i> = {age_p_cum.iloc[0]}",
    xref="paper", yref="paper",
    x=1, y=1.05,  # Position it in the upper right corner
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

# Define letter annotations based on age
letters_cum = []
if age_cum == 21:
    letters_cum = ['b', 'b', 'a']


# Add letter annotations to the BWG chart
for i, letter_cum in enumerate(letters_cum):
    fig_FCR_cum.add_annotation(
        text=letter_cum,
        x=aggregated_data_no_age_cum['TR'][i],
        y=aggregated_data_no_age_cum[y][i] + error_y_cum.iloc[i] * 1.8,  # Position above the error bar
        showarrow=False,
        font=dict(
            size=14,
            color="black"
        ),
        align="center"
    )

col8.plotly_chart(fig_FCR_cum)



###########


#carcass


st.markdown('------------')
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use the custom CSS class to center the subheader
st.markdown('<h2 class="center-text">Carcass</h2>', unsafe_allow_html=True)


# Load the data from the Excel file
df5 = pd.read_excel("sergio_study.xlsx", sheet_name='Carcass')
df6 = pd.read_excel("sergio_study.xlsx", sheet_name='P_carcass')

# Directly filter the dataframe based on all columns
filtered_data = df5.copy()

# Map treatment codes to names
if 'TR' in filtered_data.columns:
    filtered_data['TR'] = filtered_data['TR'].map({1: 'IM', 2: 'Availa-iso', 3: 'Availa-high'})

# Aggregate the data to get the mean for each treatment
aggregated_data_carc = filtered_data.groupby('TR', as_index=False).mean().round(3)
aggregated_data_carc_noTR = filtered_data.drop(columns=['TR'])

# Display the mean values grouped by treatment
st.write("Average Values by Treatment")

# Display options in table
def Home():
    with st.expander('Choose the variables'):
        showData = st.multiselect('Select Columns to Display', aggregated_data_carc.columns, default=[])
        if showData:
            st.write(aggregated_data_carc[showData])
        else:
            st.write("Select columns to display data")

# Call the Home function to display the table
Home()

st.sidebar.header('Select carcass part')

carcass = st.sidebar.selectbox('Select carcass part', aggregated_data_carc_noTR.columns, index=0)
carcass_p = df6[carcass].iloc[0].round(3)
error_y_carc = filtered_data.groupby('TR')[carcass].std()

# Plot Body Weight Gain (BWG) using Plotly
fig_carcass = px.bar(
    aggregated_data_carc, x='TR', y=carcass,title=carcass,
    color='TR', color_discrete_map=color_map,
    category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
    error_y=error_y_carc)


# Update the layout to center the title
fig_carcass.update_layout(
    title={
        'text': carcass,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    template="plotly_white",
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis=dict(
        showgrid=False,
        range=[filtered_data[carcass].min() * 0.9, filtered_data[carcass].max() *1.05]
    )
)

fig_carcass.add_annotation(
    text=f"<i>P</i> = {carcass_p}",
    xref="paper", yref="paper",
    x=1, y=1.05,
    showarrow=False,
    font=dict(
        size=14,
        color="black"
    ),
    align="right"
)

st.plotly_chart(fig_carcass)



