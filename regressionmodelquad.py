import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the dataset and add the new data points
data = {
    'Checks': [3, 5, 7, 8, 10, 10, 10, 9],
    'Downlink_Period': [20, 35, 45, 55, 75, 126, 20, 30],
    'Difference_mA': [7.26, 7.33, 9.33, 10.98, 8.59, 6.89, 70.6, 26.3]
}

df = pd.DataFrame(data)

# Add the 'Checks to Downlink Ratio' and its square for quadratic fitting
df['Checks_to_Downlink'] = df['Checks'] / df['Downlink_Period']
df['Checks_to_Downlink_Squared'] = df['Checks_to_Downlink'] ** 2

# Define independent variables (X) and dependent variable (Y)
X = df[['Checks_to_Downlink', 'Checks_to_Downlink_Squared']]
Y = df['Difference_mA']

# Fit quadratic regression model
reg = LinearRegression()
reg.fit(X, Y)

# Get coefficients for the quadratic fit
intercept = reg.intercept_
coef_ratio, coef_ratio_squared = reg.coef_

# Print the quadratic model equation
print(f"Quadratic Fit Equation: Difference_mA = {intercept:.2f} + "
      f"{coef_ratio:.2f} * Ratio + {coef_ratio_squared:.2f} * Ratio^2")

# Plotting the 3D scatter of data points
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['Downlink_Period'], df['Checks'], df['Difference_mA'], color='blue', label='Power Budget Tests')

# Create a meshgrid for plotting the quadratic surface
downlink_range = np.linspace(df['Downlink_Period'].min(), df['Downlink_Period'].max(), 20)
checks_range = np.linspace(df['Checks'].min(), df['Checks'].max(), 20)
downlink_grid, checks_grid = np.meshgrid(downlink_range, checks_range)

# Calculate the ratio and the quadratic surface
ratio_grid = checks_grid / downlink_grid
ratio_grid_squared = ratio_grid ** 2
difference_surface = (intercept +
                      coef_ratio * ratio_grid +
                      coef_ratio_squared * ratio_grid_squared)

# Plot the quadratic surface
ax.plot_surface(downlink_grid, checks_grid, difference_surface, color='green', alpha=0.6)

# Set labels and limits
ax.set_xlabel('Downlink Period (min)')
ax.set_ylabel('Checks')
ax.set_zlabel('Difference (mA)')
ax.set_title("Power Budget Regression Surface, Summer-Fall 2024")

# Add legend
scatter_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Power Budget Tests')
ax.legend(handles=[scatter_legend])

# Calculate R^2 value for the quadratic fit
r_squared = reg.score(X, Y)
print(f"R^2 value for the quadratic fit: {r_squared:.4f}")

plt.show()



