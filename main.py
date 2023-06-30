import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import bar_chart_race as bcr
from plotly.subplots import make_subplots

st.title ('COVID-19 Data Analysis and Visualization')
st.markdown("Welcome to our COVID-19 Data Analysis and Visualization Dashboard! Track the pandemic's progress with real-time data updates, interactive visualizations, and comparative analysis. Gain global and regional insights, customize charts and graphs, and access predictive analytics. Stay informed, stay safe!")

#load dataset
dfd = pd.read_csv(r"C:\Users\LENOVO\Documents\covid-19\worldometer_coronavirus_daily_data.csv")
dfs = pd.read_csv(r"C:\Users\LENOVO\Documents\covid-19\worldometer_coronavirus_summary_data.csv")

#graphs plotting
dfs["mortality_rate"] = dfs["total_deaths"]/dfs["population"]*100
fig = px.bar(dfs, x="country", y="mortality_rate", title="Mortality Rate by Countries",color ="continent")
fig.update_layout( xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig)
st.markdown("Mortality rate, or death rate, is a measure of the number of deaths (in general, or due to a specific cause) in a particular population, scaled to the size of that population, per unit of time.")    

dfs["fatality_rate"] = dfs["total_deaths"]/dfs["total_confirmed"]*100
fig1 = px.bar(dfs, x="country", y="fatality_rate", title="Fatality Rate by Countries",color="continent")
fig1.update_layout( xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig1)
st.markdown('In epidemiology, a case fatality risk or case-fatality ratio – is the proportion of deaths from a certain disease compared to the total number of people diagnosed with the disease for a particular period. A CFR is conventionally expressed as a percentage and represents a measure of disease severity.')

st.markdown("**Worldwide Coronavirus Cases**")

def choropleth(Stats,ColorbarTitle,GraphTitle):

    fig = go.Figure(data=go.Choropleth(
        locations = dfs['country'],
        locationmode='country names',
        z = Stats,
        text = dfs['country'],
        colorscale = 'reds',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = ColorbarTitle,
        ))

    fig.update_layout(
        title_text= GraphTitle,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
   
    )
    return fig

fig2 = choropleth(dfs["total_confirmed"],"Confirmed Cases","Coronavirus Confirmed Cases by Countries")
st.plotly_chart(fig2)

fig3 = choropleth(dfs["total_deaths"],"Deaths","Coronavirus Total Deaths by Countries")
st.plotly_chart(fig3)

fig4 = choropleth(dfs["total_recovered"],"Recovered Cases","Coronavirus Recovered Cases")
st.plotly_chart(fig4)

fig5 = choropleth(dfs["active_cases"],"Active Cases","Coronavirus Active Cases")
st.plotly_chart(fig5)

st.markdown("**Coronavirus Cases by Continent**")

cts = dfs.groupby("continent",as_index=False)[["total_confirmed","total_deaths","total_recovered","active_cases","serious_or_critical"]].sum()
africa = cts[cts["continent"]=="Africa"]
asia = cts[cts["continent"]=="Asia"]
ao = cts[cts["continent"]=="Australia/Oceania"]
eu = cts[cts["continent"]=="Europe"]
na = cts[cts["continent"]=="North America"]
sa = cts[cts["continent"]=="South America"]

def pie_chart(continent,text):
    trace = go.Pie(labels=['Total Confirmed','Total Deaths','Total Recovered', 'Total Active','Critical Cases'],
               values=[continent.total_confirmed.sum(),continent.total_deaths.sum(),continent.total_recovered.sum(), continent.active_cases.sum(),continent.serious_or_critical.sum()], 
               title_font_size=20,
               hovertemplate="<b>%{label}</b><br>%{value}<br><i>%{percent}</i>",
               textinfo='percent',
               textposition='inside',
               showlegend=True,
               name='',
               marker=dict(colors=["#ff5148", "#000201", "#61f7ff","#ffb861","#61ffb8"],
               line=dict(color='#000000', width=2)
               
                          )
              )
    fig=go.Figure(data=[trace])
    fig.update_layout(title_text=text)
    return fig

fig6 = pie_chart(africa,"Coronavirus Cases in Africa")
st.plotly_chart(fig6)

fig7 = pie_chart(asia,"Coronavirus Cases in Asia")
st.plotly_chart(fig7)

fig8 = pie_chart(ao,"Coronavirus cases in Australia/Oceania")
st.plotly_chart(fig8)

fig9 = pie_chart(eu,"Coronavirus Cases in Europe")
st.plotly_chart(fig9)

fig10 = pie_chart(na,"Coronavirus Cases in North America")
st.plotly_chart(fig10)

fig11 = pie_chart(sa,"Coronavirus Cases in South America")
st.plotly_chart(fig11)

st.markdown("**Countries Worst Affected by Coronavirus and Statistics**")

topdeath = dfs.sort_values(by="total_deaths" ,ascending=False)

def graphstat(cname):

    fig1 = px.line(data_frame = dfd[dfd["country"]== cname], x="date", y="cumulative_total_cases",title = "Coronavirus Total Cases in USA")
    fig2 = px.line(data_frame = dfd[dfd["country"]== cname], x="date", y="daily_new_cases",title = "Coronavirus Total Cases in USA")
    fig3 = px.line(data_frame = dfd[dfd["country"]== cname], x="date", y="cumulative_total_deaths",title = "Coronavirus Total Cases in USA")
    fig4 = px.line(data_frame = dfd[dfd["country"]== cname], x="date", y="daily_new_deaths",title = "Coronavirus Total Cases in USA")

    trace1 = fig1['data'][0]
    trace2 = fig2['data'][0]
    trace3 = fig3['data'][0]
    trace4 = fig4['data'][0]

    fig = make_subplots(rows=4, cols=1, shared_xaxes=False,subplot_titles=('Coronavirus Total Cases in '+ str(cname),'Coronavirus Daily Cases in '+str(cname),'Coronavirus Total Deaths in '+str(cname),'Coronavirus Daily Deaths in '+str(cname)))
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=2, col=1)
    fig.add_trace(trace3, row=3, col=1)
    fig.add_trace(trace4, row=4, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_xaxes(title_text="Date", row=4, col=1)

    
    fig.update_yaxes(title_text="Number of People", row=1, col=1)
    fig.update_yaxes(title_text="Number of People", row=2, col=1)
    fig.update_yaxes(title_text="Number of People", row=3, col=1)
    fig.update_yaxes(title_text="Number of People", row=4, col=1)
    
    fig.update_layout(title_text="Coronavirus Statistics in "+str(cname), height=1500)
    return fig

fig12 = graphstat("USA")
st.plotly_chart(fig12)

fig13 = graphstat("Brazil")
st.plotly_chart(fig13)

fig14 = graphstat("Mexico")
st.plotly_chart(fig14)

fig15 = graphstat("India")
st.plotly_chart(fig15)

fig16 = graphstat("UK")
st.plotly_chart(fig16)

fig17 = graphstat("Italy")
st.plotly_chart(fig17)

fig18 = graphstat("Russia")
st.plotly_chart(fig18)

fig19 = graphstat("France")
st.plotly_chart(fig19)

fig20 = graphstat("Germany")
st.plotly_chart(fig20)

fig21 = graphstat("Spain")
st.plotly_chart(fig21)

fig22 = graphstat("Iran")
st.plotly_chart(fig22)

fig23 = graphstat("Colombia")
st.plotly_chart(fig23)

fig24 = graphstat("Argentina")
st.plotly_chart(fig24)

fig25 = graphstat("South Africa")
st.plotly_chart(fig25)

fig26 = graphstat("Peru")
st.plotly_chart(fig26)

fig27 = graphstat("Poland")
st.plotly_chart(fig27)

fig28 = graphstat("Indonesia")
st.plotly_chart(fig28)

fig29 = graphstat("Turkey")
st.plotly_chart(fig29)

fig30 = graphstat("Ukraine")
st.plotly_chart(fig30)

fig31 = graphstat("Czech Republic")
st.plotly_chart(fig31)

st.markdown("**Countries Bar Chart Race**")

st.video(r"C:\Users\LENOVO\Documents\covid-19\video1.mp4")
st.video(r"C:\Users\LENOVO\Documents\covid-19\video2.mp4")