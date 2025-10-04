import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("car-sales.csv")

print("First 5 rows of the dataset:")
print(df.head())

print("\nDataset info:")
print(df.info())

sales_by_model = df.groupby('Model')['Sales_in_thousands'].sum().sort_values(ascending=False)

top_10 = sales_by_model.head(10)

print("\nTop 10 Car Models by Sales:")
print(top_10)

plt.figure(figsize=(10,6))
top_10.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Top 10 Car Models by Sales')
plt.xlabel('Car Model')
plt.ylabel('Sales (in thousands)')
plt.xticks(rotation=45, fontsize=10)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,12))
sales_by_model.plot(kind='barh', color='lightcoral', edgecolor='black')
plt.title('Car Sales by Model (All)')
plt.xlabel('Sales (in thousands)')
plt.ylabel('Car Model')
plt.gca().invert_yaxis()  
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,8))
top_10.plot(
    kind='pie', 
    autopct='%1.1f%%', 
    startangle=140, 
    counterclock=False,
    wedgeprops={'edgecolor':'black'}
)
plt.title('Sales Distribution (Top 10 Models)')
plt.ylabel('')
plt.tight_layout()
plt.show()

fig_bar = px.bar(
    top_10,
    x=top_10.index,
    y=top_10.values,
    title="Top 10 Car Models by Sales (Interactive)",
    labels={'x':'Car Model','y':'Sales (in thousands)'},
    text=top_10.values,
    color=top_10.values,
    color_continuous_scale='Blues'
)
fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig_bar.update_layout(xaxis_tickangle=45)
fig_bar.show()

fig_pie = px.pie(
    top_10,
    names=top_10.index,
    values=top_10.values,
    title="Sales Distribution by Top 10 Car Models (Interactive)",
    hole=0.3
)
fig_pie.update_traces(textinfo='percent+label')
fig_pie.show()
