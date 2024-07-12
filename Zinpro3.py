

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

# Set page configuration
st.set_page_config(page_title='Zinpro', page_icon='Zinpro', layout='wide')
st.sidebar.image("Zinpro.png", caption='Zinpro Availa')

with st.container():
    st.markdown(
        """
        <style>
        .fixed-title {
            position: fixed;
            top: 0;
            width: 100%;
            background-color: white;
            z-index: 9999;
            padding: 30px 0;
            border-bottom: 1px solid #ddd;
        }
        .content {
            margin-top: 10px; /* Adjust this value to add more space below the title */
        }
        .header {
            color: #00009e;
            font-size: 4em;
            font-weight: bold;
            text-align: left;
        }
        .subheader {
            color: #000000;
            font-size: 1.5em;
            font-weight: bold;
            text-align: left;
        }
        .center-text {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Fixed title
    st.markdown(
        '<div class="fixed-title"><h1 class="header">Zinc and Chrome Study</h1><h2 class="subheader">Effects of Availa Zinc Chrome Inclusion in Broilers Diets</h2></div>',
        unsafe_allow_html=True)

    # Main content with scrollbar
    st.markdown('<div class="content">', unsafe_allow_html=True)


#########



# Load the data from an Excel file
df = pd.read_excel("sergio_study.xlsx", sheet_name='Age', na_values='NaN')
df['BWG'] = df["BWG"] / 1000
df2 = pd.read_excel("sergio_study.xlsx", sheet_name='P')


# Define the color map
color_map = {'IM': '#000000', 'Availa-iso': '#000061', 'Availa-high': '#00009e'}



def graphs_performance():
    # Use the custom CSS class to center the subheader
    # Define the custom CSS for centering text
    st.markdown(
        """
        <style>
        .center-text {
            text-align: center;
            margin-top: 30px; /* Adjust this value as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Use the custom CSS class to center the subheader
    st.markdown('<h2 class="center-text">Performance by Age</h2>', unsafe_allow_html=True)

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
        title={
            'text': 'Feed Conversion Ratio',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        template="plotly_white",
        plot_bgcolor="white",
        paper_bgcolor='white',
        yaxis=dict(
            showgrid=False,  # Hide horizontal grid lines
            range=[age_filtered[y].min() * 0.9, age_filtered[y].max() + age_filtered[y].std()]
            # Set the range of the Y-axis
        ),
        width=900,  # Set the desired width
        height=500,  # Set the desired height
        margin=dict(l=350)  # Adjust the left margin to shift the chart to the right
    )

    p_value_fcr = age_p.iloc[0]
    annotation_text = "<i>P</i> < 0.001" if p_value_fcr < 0.001 else f"<i>P</i> = {p_value_fi}"

    fig_FCR.add_annotation(
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
        letters = ['b', 'b', 'a']
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

#graphs_performance()

#st.markdown('------------')

##############################################

df3 = pd.read_excel("sergio_study.xlsx", sheet_name='Cumulative', na_values='NaN')
df4 = pd.read_excel("sergio_study.xlsx", sheet_name='P_cumulative', na_values='NaN')



#st.subheader('Cumulative Age')



######charts

# Plot Body Weight Gain (BWG) using Plotly
#col6, col7 = st.columns(2)
#col8, col9 = st.columns(2)

def graphs_cumulative():
    # Use the custom CSS class to center the subheader
    st.markdown(
        """
        <style>
        .center-text {
            text-align: center;
            margin-top: 30px; /* Adjust this value as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h2 class="center-text">Performance by Cumulative Age</h2>', unsafe_allow_html=True)

    # Sidebar for selecting cumulative age
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

    # Create columns for the plots
    col1, col2 = st.columns(2)
    col3, = st.columns(1)

    # Plot Body Weight Gain (BWG) using Plotly
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

    col1.plotly_chart(fig_bwg_cum)

    # Plot Feed Intake (FI) using Plotly
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

    # Add letter annotations to the FI chart
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

    col2.plotly_chart(fig_FI_cum)

    # Plot Feed Conversion Ratio (FCR) using Plotly
    y = 'FCR'
    age_p_cum = df4[df4['Age'] == age_cum].loc[:, y].round(3)
    error_y_cum = age_filtered_cum.groupby('TR')[y].std()

    fig_FCR_cum = px.bar(aggregated_data_no_age_cum, x='TR', y=y, title='Feed Conversion Ratio',
                         color='TR', color_discrete_map=color_map,
                         category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                         error_y=error_y_cum)

    fig_FCR_cum.update_layout(
        title={
            'text': 'Feed Conversion Ratio',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        template="plotly_white",
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(
            showgrid=False,  # Hide horizontal grid lines
            range=[age_filtered_cum[y].min() * 0.9, age_filtered_cum[y].max() + age_filtered_cum[y].std()]
            # Set the range of the Y-axis
        ),
        width=900,  # Set the desired width
        height=500,  # Set the desired height
        margin=dict(l=350)  # Adjust the left margin to shift the chart to the right
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

    # Add letter annotations to the FCR chart
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

    col3.plotly_chart(fig_FCR_cum)

#graphs_cumulative()

###########


#carcass

    # Load the data from the Excel file
df5 = pd.read_excel("sergio_study.xlsx", sheet_name='Carcass')
df6 = pd.read_excel("sergio_study.xlsx", sheet_name='P_carcass')


with st.container():
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
def Table_carc():
    # Define custom CSS for margin

    with st.expander('Select one or more variables to display in the table'):
        showData = st.multiselect('Select Columns to Display', aggregated_data_carc.columns, default=[])
        if showData:
            # Add a div with the custom class around the table
            st.markdown('<div class="margined-content">', unsafe_allow_html=True)
            st.write(aggregated_data_carc[showData])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("Select one or more variables to display in the table")


def graphs_carcass():
    with st.container():
        st.markdown('------------')
        st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                #margin-top: 0px; /* Adjust this value as needed */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Use the custom CSS class to center the subheader
        st.markdown('<h2 class="center-text">Carcass</h2>', unsafe_allow_html=True)



    with st.container():
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
        Table_carc()
    with st.container():
        st.sidebar.header('Carcass variables')
        carcass = st.sidebar.selectbox('Select one variable', aggregated_data_carc_noTR.columns, index=0)
        carcass_p = df6[carcass].iloc[0].round(3)
        error_y_carc = filtered_data.groupby('TR')[carcass].std()

    # Display options in table

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
            range=[filtered_data[carcass].min() * 0.9, filtered_data[carcass].max() * 1.05]
        ),
        width=900,  # Set the desired width
        height=600,  # Set the desired height
        margin=dict(l=350)  # Adjust the left margin to shift the chart to the right
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
#graphs_carcass()

#########
# Define the sidebar function
# Define the sidebar function
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',
            options=['Performance by age', 'Performance cumulative', 'Carcass'],
            icons=['house', 'house', 'house'],
            menu_icon='cast',
            default_index=0
        )

    if selected == 'Performance by age':
        #st.subheader(f"Page: {selected}")
        graphs_performance()
    elif selected == 'Performance cumulative':
        #st.subheader(f"Page: {selected}")
        graphs_cumulative()
    elif selected == 'Carcass':
        #st.subheader(f"Page: {selected}")
        graphs_carcass()
        #Home()




# Call the sidebar function within the Streamlit app
sideBar()
