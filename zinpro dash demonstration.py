# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:59:31 2024

@author: marco
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import numpy as np

st.set_page_config(page_title='Zinpro', page_icon='Zinpro', layout='wide')
st.sidebar.image("Zinpro.png", caption='Zinpro Availa')

def broiler():
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
            '<div class="fixed-title"><h1 class="header">Zinc and Chrome Study</h1><h2 class="subheader">Effects of Isoferm Inclusion in Broilers Diets</h2></div>',
            unsafe_allow_html=True)

        # Main content with scrollbar
        st.markdown('<div class="content">', unsafe_allow_html=True)


    @st.cache_data
    def load_data():
        # Load the data from an Excel file
        df = pd.read_excel("sergio_study.xlsx", sheet_name='Age', na_values='NaN')
        df['BWG'] = df["BWG"] / 1000
        df2 = pd.read_excel("sergio_study.xlsx", sheet_name='P')
        df3 = pd.read_excel("sergio_study.xlsx", sheet_name='Cumulative', na_values='NaN')
        df4 = pd.read_excel("sergio_study.xlsx", sheet_name='P_cumulative', na_values='NaN')
        df5 = pd.read_excel("sergio_study.xlsx", sheet_name='Carcass')
        df6 = pd.read_excel("sergio_study.xlsx", sheet_name='P_carcass')

        return df, df2, df3, df4, df5, df6


    # Load the data
    df, df2, df3, df4, df5, df6 = load_data()

    # Define the color map
    color_map = {'IM': '#000000', 'Availa-iso': '#000061', 'Availa-high': '#00009e'}


    def graphs_performance():
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

        # Track the current column for plotting
        current_column = col1

        for idx, col_name in enumerate(df.columns[1:]):
            # Ensure df2 has the column before proceeding
            if col_name in df2.columns:
                # Plot using Plotly
                y = col_name
                age_p = df2[df2['Age'] == age].loc[:, y].round(3)
                error_y = age_filtered.groupby('TR')[y].std()

                fig = px.bar(aggregated_data_no_age, x='TR', y=y, title=col_name,
                             color='TR', color_discrete_map=color_map,
                             category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                             error_y=error_y)

                fig.update_layout(
                    template="plotly_white",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    yaxis=dict(
                        showgrid=False,  # Hide horizontal grid lines
                        range=[age_filtered[y].min() * 0.9, age_filtered[y].max() + age_filtered[y].std()]
                        # Set the range of the Y-axis
                    )
                )

                p_value = age_p.iloc[0]
                annotation_text = "<i>P</i> < 0.001" if p_value < 0.001 else f"<i>P</i> = {p_value}"

                fig.add_annotation(
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

                # Add letter annotations to the chart
                for i, letter in enumerate(letters):
                    fig.add_annotation(
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

                # Alternate between columns for each chart
                if current_column == col1:
                    col1.plotly_chart(fig)
                    current_column = col2
                else:
                    col2.plotly_chart(fig)
                    current_column = col1

    def graphs_cumulative():
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

        # Track the current column for plotting
        current_column = col1

        for idx, col_name in enumerate(df3.columns[1:]):
            # Ensure df4 has the column before proceeding
            if col_name in df4.columns:
                # Plot using Plotly
                y = col_name
                age_p_cum = df4[df4['Age'] == age_cum].loc[:, y].round(3)
                error_y_cum = age_filtered_cum.groupby('TR')[y].std()

                if y == 'FI':
                    fig_carcass = px.pie(
                        aggregated_data_no_age_cum,
                        names='TR',
                        values=y,
                        title=y,
                        color='TR',
                        color_discrete_map=color_map,
                        category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']}
                    )
                    st.plotly_chart(fig_carcass)
                else:
                    fig = px.bar(aggregated_data_no_age_cum, x='TR', y=y, title=col_name,
                                 color='TR', color_discrete_map=color_map,
                                 category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
                                 error_y=error_y_cum)

                    fig.update_layout(
                        template="plotly_white",
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        yaxis=dict(
                            showgrid=False,  # Hide horizontal grid lines
                            range=[age_filtered_cum[y].min() * 0.9, age_filtered_cum[y].max() + age_filtered_cum[y].std()]
                            # Set the range of the Y-axis
                        )
                    )

                    p_value = age_p_cum.iloc[0]
                    annotation_text = "<i>P</i> < 0.001" if p_value < 0.001 else f"<i>P</i> = {p_value}"

                    fig.add_annotation(
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
                    if age_cum == 21:
                        letters = ['a', 'b', 'b']
                    elif age_cum == 34:
                        letters = ['b', 'b', 'a']

                    # Add letter annotations to the chart
                    for i, letter in enumerate(letters):
                        fig.add_annotation(
                            text=letter,
                            x=aggregated_data_no_age_cum['TR'][i],
                            y=aggregated_data_no_age_cum[y][i] + error_y_cum.iloc[i] * 1.8,  # Position above the error bar
                            showarrow=False,
                            font=dict(
                                size=14,
                                color="black"
                            ),
                            align="center"
                        )

                    # Alternate between columns for each chart
                    if current_column == col1:
                        col1.plotly_chart(fig)
                        current_column = col2
                    else:
                        col2.plotly_chart(fig)
                        current_column = col1

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
            aggregated_data_carc, x='TR', y=carcass, title=carcass,
            color='TR', color_discrete_map=color_map,
            category_orders={'TR': ['IM', 'Availa-iso', 'Availa-high']},
            error_y=error_y_carc)

        # Update the layout to center the title

        fig_carcass.update_layout(
            title={
                'text': carcass,
                'y': 0.9,
                'x': 0.5,
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

    def Table_carc():
        with st.expander('Select one or more variables to display in the table'):
            showData = st.multiselect('Select Columns to Display', aggregated_data_carc.columns, default=[])
            if showData:
                st.write(aggregated_data_carc[showData])
            else:
                st.write("Select one or more variables to display in the table")

    def sideBar():
        selected = option_menu(
            menu_title='Broiler Menu',
            options=['Performance by age', 'Performance cumulative', 'Carcass'],
            icons=['bar-chart-line', 'bar-chart-steps', 'clipboard-data'],
            menu_icon='cast',
            default_index=0,
            orientation='horizontal'
        )

        if selected == 'Performance by age':
            graphs_performance()
        elif selected == 'Performance cumulative':
            graphs_cumulative()
        elif selected == 'Carcass':
            graphs_carcass()

    sideBar()

def laying_hens():
    def data_laying():
        d = 20.8831
        a = 102.7
        b = 0.00244
        c = 1.3763

        d2 = 20.8831
        a2 = 102.7
        b2 = 0.00244
        c2 = 1.3763

        d3 = 20.8815
        a3 = 101.9
        b3 = 0.00212
        c3 = 1.377

        d4 = 20.8792
        a4 = 101.4
        b4 = 0.00193
        c4 = 1.3799

        d5 = 20.6282
        a5 = 102.4
        b5 = 0.00242
        c5 = 1.4434

        d6 = 20.6304
        a6 = 102.0
        b6 = 0.00221
        c6 = 1.4378

        d7 = 20.6201
        a7 = 100.4
        b7 = 0.00169
        c7 = 1.4547

        d8 = 20.6220
        a8 = 101.0
        b8 = 0.00191
        c8 = 1.4524

        week = np.arange(18, 90, 1)

        EO_maq1 = {'week': week, 'Treatment': 'IM', 'indice': 1,
                   'EO': a * np.exp(-b * week) / (1 + np.exp(-c * (week - d)))}
        EO_maq2 = {'week': week, 'Treatment': 'AACM2', 'indice': 2,
                   'EO': a2 * np.exp(-b2 * week) / (1 + np.exp(-c2 * (week - d2)))}
        EO_maq3 = {'week': week, 'Treatment': 'AACM3', 'indice': 3,
                   'EO': a3 * np.exp(-b3 * week) / (1 + np.exp(-c3 * (week - d3)))}
        EO_maq4 = {'week': week, 'Treatment': 'AACM4', 'indice': 4,
                   'EO': a4 * np.exp(-b4 * week) / (1 + np.exp(-c4 * (week - d4)))}
        EO_maq5 = {'week': week, 'Treatment': 'AACM5', 'indice': 5,
                   'EO': a5 * np.exp(-b5 * week) / (1 + np.exp(-c5 * (week - d5)))}
        EO_maq6 = {'week': week, 'Treatment': 'AACM6', 'indice': 6,
                   'EO': a6 * np.exp(-b6 * week) / (1 + np.exp(-c6 * (week - d6)))}
        EO_maq7 = {'week': week, 'Treatment': 'AACM7', 'indice': 7,
                   'EO': a7 * np.exp(-b7 * week) / (1 + np.exp(-c7 * (week - d7)))}
        EO_maq8 = {'week': week, 'Treatment': 'AACM8', 'indice': 8,
                   'EO': a8 * np.exp(-b8 * week) / (1 + np.exp(-c8 * (week - d8)))}

        EO = pd.concat([pd.DataFrame(EO_maq1), pd.DataFrame(EO_maq2), pd.DataFrame(EO_maq3), pd.DataFrame(EO_maq4),
                        pd.DataFrame(EO_maq5), pd.DataFrame(EO_maq6), pd.DataFrame(EO_maq7), pd.DataFrame(EO_maq8)],
                       keys=['IM', 'AACM2', 'AACM3', 'AACM4', 'AACM5', 'AACM6', 'AACM7', 'AACM8'])

        return EO

    # Load the data
    EO = data_laying()

    st.title("Laying Hens - long study egg production")

    # Add a slider to select the range of weeks
    min_week, max_week = int(EO['week'].min()), int(EO['week'].max())
    selected_weeks = st.sidebar.slider("Select week range:", min_week, max_week, (min_week, max_week))

    # Filter the data based on the selected week range
    filtered_data = EO[(EO['week'] >= selected_weeks[0]) & (EO['week'] <= selected_weeks[1])]

    # Create a line plot
    fig = px.line(filtered_data, x='week', y='EO', color='Treatment', title='EO Over Weeks',
                  labels={'week': 'Week', 'EO': 'EO'},
                  template='plotly_white')

    # Update layout for better aesthetics
    fig.update_layout(
        xaxis_title='Week',
        yaxis_title='EO',
        legend_title_text='Treatment',
        xaxis=dict(
            title_font=dict(size=20),
            tickfont=dict(size=15)
        ),
        yaxis=dict(
            title_font=dict(size=20),
            tickfont=dict(size=15)
        ),
        width=1200,
        height=800
    )

    st.plotly_chart(fig)

def broiler_breed():
    def data_broiler_breed():
        day = np.arange(130, 191, 1)
        AACM1 = 96.9684 * np.exp(-np.exp(-0.1530 * (day - 144.4)))
        IM1 = 97.9281 * np.exp(-np.exp(-0.1416 * (day - 146.1)))

        Treatment_IM = np.repeat('IM', (191 - 130))
        Treatment_AACM = np.repeat('AACM', (191 - 130))

        data_IM = {'Day': day, 'EO': IM1, 'Treatment': Treatment_IM}
        data_AACM = {'Day': day, 'EO': AACM1, 'Treatment': Treatment_AACM}

        df_IM = pd.DataFrame(data_IM)
        df_AACM = pd.DataFrame(data_AACM)

        EO = pd.concat([df_IM, df_AACM], ignore_index=True)

        return EO

    # Load the data
    EO = data_broiler_breed()

    st.title("Broiler Breed - EO Over Weeks")

    # Add a slider to select the range of days
    min_day, max_day = int(EO['Day'].min()), int(EO['Day'].max())
    selected_days = st.slider("Select week range:", min_day, max_day, (min_day, max_day))

    # Filter the data based on the selected day range
    filtered_data = EO[(EO['Day'] >= selected_days[0]) & (EO['Day'] <= selected_days[1])]

    # Create a bubble chart
    fig = px.scatter(filtered_data, x='Day', y='EO', color='Treatment', size='EO', title='EO Over Days',
                     labels={'Day': 'Day', 'EO': 'EO'},
                     template='plotly_white')

    # Update layout for better aesthetics, including axis font sizes
    fig.update_layout(
        xaxis_title='Weeks',
        yaxis_title='Egg output',
        legend_title_text='Treatment',
        xaxis=dict(
            title_font=dict(size=20),
            tickfont=dict(size=15)
        ),
        yaxis=dict(
            title_font=dict(size=20),
            tickfont=dict(size=15)
        ),
        width=900,
        height=600
    )

    st.plotly_chart(fig)

def General():
    with st.sidebar:
        selected = option_menu(
            menu_title='Main Menu',
            options=['Laying hens', 'Broiler', 'Broiler breed'],
            icons=['egg-fried', 'chicken', 'leaf'],
            menu_icon='cast',
            default_index=0
        )
    if selected == 'Laying hens':
        laying_hens()
    elif selected == 'Broiler':
        broiler()
        # Add broiler function call here
    elif selected == 'Broiler breed':
        broiler_breed()
        # Add broiler breed function call here

General()






