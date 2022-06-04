import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#Preprocessing
df = pd.read_csv("data/Coffee Chain.csv")
df["Inventory"]=df["Inventory"].str.replace(",","").astype(int)
#Reading in the Lat/long which the original data didnt have(got it from Tableau)
df1=pd.read_csv("data/areadata.csv")
#merging the  two data sets
newdf=pd.merge(df,df1, on='Area Code', how='outer')


st.title("Coffee Chain Dashboard")



time_frame = st.selectbox("View by: ", ("Product", "Product Type","Market"),0)

if time_frame=="Product":
    selectdata="Product"
elif time_frame=="Product Type":
    selectdata="Product Type"
else:
    selectdata="Market"
st.text("Bubble size equal Coffee Sales")
#the plot

fig1 = px.scatter_geo(
    newdf,
    lat=newdf["Latitude (generated)"],
    lon=newdf["Longitude (generated)"],

    scope="usa",
    color=selectdata,

    hover_name= "State",
    hover_data=["Area Code"],

    size="Coffee Sales",



color_continuous_scale=px.colors.sequential.YlOrRd,

        template='plotly_dark',
        locationmode= "USA-states"
        )
fig1.update_layout(width=1000,height=700)

st.plotly_chart(fig1)



# Inventory count by store
value=st.number_input("Type in the Area Code for the Store Inventory Count",value=970,step=None,key=newdf["Area Code"].unique())
filt=newdf["Area Code"]==value
aproduct=newdf.loc[filt].groupby(["Product"])["Inventory"].sum().sort_values()
#the inventory chart
fig=px.bar(aproduct,color= aproduct,title="Product inventory for the coffee shop in Area Code: " + str(value) +"",orientation="h",
labels={"color":"Inventory levels"})


fig.update_layout(width=900,height=700)

st.plotly_chart(fig)
