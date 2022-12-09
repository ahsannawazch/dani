# Importing Libraries

import pandas as pd
import streamlit as st 
import plotly.express as px 
from src import plotting,reading_data,filter_data

st.title("Drive Testing Data Analysis")


#Streamlit file uploader 
datafile = st.file_uploader(" CSV or xlsx files are supported at the moment")


# st.button()
total_cols = st.number_input("Enter the total no. of columns for analysis",key="col_count",min_value=1)

for n in range(total_cols):
    st.write("Analysis of Column",n+1)

    if datafile: 
        def filterandplotting(datafile):

                df = reading_data(datafile)

                col_name = st.selectbox("Select the desired parameter(s) for analysis", 
                                ('Rsrp','SNR','Rsrq','4g Data Throughput','3g Data Throughput','2g Data Throughput',
 '2g CST', '3g CST','4g CST','Rx level','Rx qual','Rscp','Ecno'),key="col_name "+ str(n))
                                       
                threshold = st.number_input("Enter the threshold/criteria",key= "threshold "+ str(n),value=-90,step=1)
                cluster_members = st.number_input("Cluster Members",key= "cluster_members " + str(n),help="Minimum no. of points in the cluster",value=5)

                df_out = filter_data(df,col_name,threshold,cluster_members)
                info = st.selectbox("Want to see more details",options=["No","Yes"],key="info "+ str(n))

                if info == "Yes":
                    st.write(" Filtered Data is below: ")
                    st.write(df_out)
                    st.write("Filtered data shape is" ,df_out.shape)
                    st.write("Grouped Red Points are following")
                    st.write(df_out.loc[df_out[col_name]<threshold] )
                # Calling the function to plot scatter mapbox     
                plotting(df_out,col_name,threshold )


        filterandplotting(datafile)
    st.write("______________________________________________________")