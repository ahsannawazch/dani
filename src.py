import plotly.express as px 
import streamlit as st
import pandas as pd
import os

# Function to save the file and return the df
def reading_data(file):
    if file is not None:
        file_details = {"FileName":file.name,"FileType":file.type}
        # Reading CSV type
        if file_details["FileType"] == "application/vnd.ms-excel":
            raw_data = pd.read_csv(file,index_col=0)
            st.write("CSV received") 
            
        
        # Reading xlsx type
        if file_details["FileType"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raw_data  = pd.read_excel(file,index_col=0,sheet_name=0)
            st.write("Excel file received")
            
        
        raw_data = raw_data.reset_index(drop=True)
        st.dataframe(raw_data)
        st.write(raw_data.shape)
        st.write("Data Statistics")
        st.write(raw_data.describe())

        return raw_data.reset_index(drop=True)    

        # Saving the file in ((((((tempdir))))))    
    if file:
        with open(os.path.join(file.name),"wb") as f:
            f.write(file.getbuffer())
        st.success("Saved file :{} in (##unknown)".format(file.name))

def filter_data(df, data_column,criteria,group_members):
    if data_column in df.columns:
        
        n = 2   # number of seconds
        
        #group_members = int(st.text_input(label="Cluster members",value= "5",max_chars=1,help="Minimum no. of points in the group"))

        green_df  = df.loc[df[data_column] >= criteria]
        red_df = df.loc[df[data_column] < criteria]
        #red_df= red_df.sort_values(by="Time")
        red_df["era"] = pd.to_datetime(red_df["Date"]+ " " +red_df["Time"], infer_datetime_format=True,)
        red_df = red_df.sort_values(by="era")
        #filtering out the consective bad records in the dataframe
        red_df["Group"] = red_df.era.diff().dt.seconds.gt(n).cumsum()
        group_id = red_df["Group"].value_counts()[red_df["Group"].value_counts() >= group_members].index.to_list() 
        # All records having those unique groups
        red_df = red_df.loc[red_df["Group"].isin(group_id)]      
        final_red = red_df.drop(columns=["era","Group"])
        final_df = pd.concat([green_df,final_red],ignore_index=True,axis=0)
#        st.write("The green_df shape is" ,green_df.shape)
        st.write("The cluster shape is" ,final_red.shape)
        #st.write("Filtered data shape is" ,final_df.shape)
        #st.write(" Filtered Data is below: ")
        #st.write(final_df)
        return final_df
        #final_df.to_csv("filtered rxlevels.csv")                              #####################################
    else:
        st.write(df.columns)
        st.write("column name in data should be same as mentioned in above box")
        




# Function to plot scatter mapbox of any given df and criteria
def plotting(df_plot,data_column,criteria):
    
    df_plot["category"] = df_plot.apply(lambda x: "Red" if  x[data_column] < criteria else "Green",axis=1)

    fig = px.scatter_mapbox(df_plot,
                            lat = df_plot.Latitude, 
                            lon= df_plot.Longitude,
                            color= df_plot.category,
                            width=1000, 
                            height=800, 
                            title=" Driving test map for " + str(data_column),
                            zoom=12,
                            color_discrete_map={"Green": "green", "Red":"red"},
                            hover_data = ["Latitude","Longitude",data_column]


    #                        symbol= df.Date
                            #animation_frame= df.Date,

    #                       range_color=[-90,-48]
                            )

    fig.update_layout(mapbox_style = "open-street-map")
    fig.update_layout(margin={'t':50,'b':10,'l':50,'r':50})
    st.plotly_chart(fig)

    

