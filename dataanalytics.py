import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.image('socialmedia.jpg')

st.title("📊 Social Media vs Productivity") 

df = pd.read_csv("cleandata.csv")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f3fbff;  /* pastel blue */
        color: #333333;  /* darker text for contrast */
        padding: 2rem;
    }
    /* Optional: keep content container with white bg for readability */
    .st-emotion-cache-6qob1r, .st-emotion-cache-1y4p8pa {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 10px;
        padding: 1.5rem;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Aggregated stats
mean_daily = round(df['Daily Social Media Time'].mean(), 2)
max_coffee = round(df['Coffee Consumption per Day'].max(), 2)
min_productivity = round(df['Actual Productivity Score'].min(), 2)

# Spacer
st.markdown("---")

# Most/least common platforms
most_common = df['Social Platform Preference'].value_counts().idxmax()
most_common_count = df['Social Platform Preference'].value_counts().max()

least_common = df['Social Platform Preference'].value_counts().idxmin()
least_common_count = df['Social Platform Preference'].value_counts().min()

# Layout: 3 columns for metrics
col1, col2, col3 = st.columns(3)

col1.metric("Avg. Daily Social Media Time", f"{mean_daily} hrs")
col2.metric("Max Coffee/Day", f"{max_coffee} cups")
col3.metric("Min Productivity Score", f"{min_productivity}")

# Spacer
st.markdown("---")

# Layout: 2 columns for platform preference
col4, col5 = st.columns(2)

col4.metric("Most Preferred Platform", f"{most_common}", f"{most_common_count} users")
col5.metric("Least Preferred Platform", f"{least_common}", f"{least_common_count} users")

# Spacer
st.markdown("---")

# Histogram for Job Satisfaction Scores 
st.subheader("Job Satisfaction Scores") 
column = 'Job Satisfaction Score' 
fig = px.histogram(df, x=column) 
fig.update_traces(marker={"color": "skyblue", "line": {"color": "black", "width": 1}}) 
fig.update_layout( 
    xaxis_title="Job Satisfaction Score", 
    yaxis_title="Count", 
    xaxis=dict( 
        tickmode='linear', 
        dtick=1,            # show a tick every 1 unit 
        range=[0, 10],      # adjust based on your data range 
        showgrid=True), 
    yaxis=dict( 
        tickmode='linear', 
        dtick=30,            # adjust based on your data 
        showgrid=True) 
) 
st.plotly_chart(fig) 

 

# Scatter Plot: Work Hours vs Stress Level 
st.subheader("Work Hours vs Stress Level") 
x_column = 'Work Hours per Day' 
y_column = 'Stress Level' 
fig, ax = plt.subplots(figsize=(10, 6)) 
df.plot(kind='scatter', x=x_column, y=y_column, ax=ax) 
fig = px.scatter(df, x=x_column, y=y_column, color='Gender', color_discrete_sequence=['purple', 'skyblue'])  # Optional coloring 
fig.update_layout( 
    xaxis_title="Work Hours per Day", 
    yaxis_title="Stress Level", 
    xaxis=dict( 
        tickmode='linear', 
        dtick=1,            # show a tick every 1 unit 
        range=[-0.5, 12.5],      # adjust based on your data range 
        showgrid=True), 
    yaxis=dict( 
        tickmode='linear', 
        dtick=1,            # adjust based on your data 
        showgrid=True) 
) 
st.plotly_chart(fig) 



# Pie Chart: Gender Distribution 
st.subheader("Gender Distribution") 
gender_counts = df['Gender'].value_counts() 
fig = px.pie( 
    values=gender_counts.values, 
    names=gender_counts.index, 
    color_discrete_sequence=['lightblue', 'pink'] 
) 
fig.update_traces(textposition='inside', textinfo='percent+label') 
st.plotly_chart(fig) 


# Stacked Bar Chart for Coffee Consumption vs Gender 
st.subheader("Coffee Consumption vs Gender ")
pivot_df = df.pivot_table(index='Gender', columns='Job Type', values='Coffee Consumption per Day', aggfunc='sum').fillna(0)
pivot_df = pivot_df.reindex(['Male', 'Female'])  # Optional: reorder genders
fig, ax = plt.subplots(figsize=(10, 6))
bars = pivot_df.plot(kind='bar', stacked=True, ax=ax, colormap='Pastel1')
ax.set_xlabel("Gender", fontsize=14)
ax.set_ylabel("Total Coffee Consumption", fontsize=14)
ax.legend(title='Productivity Score', fontsize=10)
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        if height > 0:
            x = bar.get_x() + bar.get_width() / 2
            y = bar.get_y() + height / 2
            ax.text(x, y, f'{height:.1f}', ha='center', va='center', fontsize=8, color='black')
totals = pivot_df.sum(axis=1)
for idx, total in enumerate(totals):
    ax.text(idx, total + 1, f'Total: {total:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
st.pyplot(fig)



# Bar Chart for Average Days Feeling Burnout per Month vs Job Type
st.subheader("Average Days Feeling Burnout per Month vs Job Type")
group_column = 'Job Type'
value_column = 'Days Feeling Burnout per Month'
avg_df = df.groupby(group_column, as_index=False)[value_column].mean()
avg_df[value_column] = avg_df[value_column].round(2)
pastel_colors = ['#A8DADC', '#FDCBBA', '#FFE0AC', '#C3B1E1', '#B5EAD7'] 
fig = px.bar(
    avg_df,
    x=group_column,
    y=value_column,
    text=value_column,
    color=group_column,
    color_discrete_sequence=pastel_colors
)
fig.update_traces(textposition='outside')
fig.update_layout(
    xaxis_title=group_column,
    yaxis_title=f"Average {value_column}",
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    showlegend=False  
)
st.plotly_chart(fig)



# Box Plot for Screen Time Before Sleep vs Social Platform
st.subheader("Screen Time Before Sleep vs Social Platform Preference")
x_column = 'Social Platform Preference'       
y_column = 'Screen Time Before Sleep'    
fig = px.box(df, x=x_column, y=y_column, color=x_column,
             title=" ",
             color_discrete_sequence=px.colors.qualitative.Pastel)
mean_values = df.groupby(x_column)[y_column].mean().round(2).reset_index()
for i, row in mean_values.iterrows():
    fig.add_trace(go.Scatter(
        x=[row[x_column]],
        y=[row[y_column]],
        mode='text',
        text=[f"{row[y_column]:.2f}"],
        textposition='top center',
        showlegend=False
    ))
fig.update_layout(
    width=900,
    height=600,
    xaxis_title=x_column,
    yaxis_title=y_column,
    title_font_size=18,
    xaxis_tickangle=45,
    font=dict(size=14)
)
fig.update_yaxes(tickformat=".2f")  # 2 decimal places
st.plotly_chart(fig)   




st.markdown("### ℹ️ Additional Information:")
st.info("💡 Studies show that people who reduce social media usage by 30 minutes a day report better focus.") 
st.warning("⚠️ Heavy usage can lead to procrastination and anxiety.") 
st.success("✅ Good practice: use screen time apps to monitor and control usage.") 


















