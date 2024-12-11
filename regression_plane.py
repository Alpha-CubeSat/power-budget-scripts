import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the dataset
data = {
    'Checks': [3, 5, 7, 8, 10, 10],
    'Downlink_Period': [20, 35, 45, 55, 75, 126],
    'Difference_mA': [7.26, 7.33, 9.33, 10.98, 8.59, 6.89]
}

Bdata = {
    'Checks': [3, 5, 10, 3, 3, 5],
    'Downlink_Period': [20, 20, 20, 20, 10, 50],
    'Difference_mA': [6.9, 16.5, 70.6, 8.7, 10.1, 6.4]
}

df = pd.DataFrame(data)
dfb = pd.DataFrame(Bdata)

# Define independent variables (X) and dependent variable (Y)
X = df[['Downlink_Period', 'Checks']]  # 'Downlink Period' as X and 'Checks' as Y for regression
Z = df['Difference_mA']  # 'Difference (mA)' as Z

# Fit linear regression model
reg = LinearRegression()
reg.fit(X, Z)

# Get coefficients for the fitted plane
intercept = reg.intercept_
coef_downlink, coef_checks = reg.coef_

# Ask the user if they want to test a pair
test_input = input("Do you want to test a Downlink Period/Checks pair? (yes/no): ").strip().lower()

# Initialize plotting variables
user_point_plotted = False
downlink_period_input = checks_input = difference_predicted = None

if test_input == "yes":
    # Ask for Downlink Period and Checks values
    downlink_period_input = float(input("Enter Downlink Period: "))
    checks_input = float(input("Enter Checks value: "))
    
    # Calculate the projected Difference_mA for the user-provided point
    difference_predicted = intercept + coef_downlink * downlink_period_input + coef_checks * checks_input
    
    # Determine PASS or FAIL
    threshold = 10.2
    status = "PASS" if difference_predicted < threshold else "FAIL"
    print(f"The predicted Difference_mA is {difference_predicted:.2f}. Status: {status}")
    
    # Set flag to plot the user point
    user_point_plotted = True

# Plotting the 3D scatter of data points
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['Downlink_Period'], df['Checks'], df['Difference_mA'], color='blue', label='F24 Data Points')
ax.scatter(dfb['Downlink_Period'], dfb['Checks'], dfb['Difference_mA'], color='red', label='SU24 Data Points')

# Create a meshgrid for plotting the regression planes
x_surf, y_surf = np.meshgrid(np.linspace(df['Downlink_Period'].min(), df['Downlink_Period'].max(), 10),
                             np.linspace(df['Checks'].min(), df['Checks'].max(), 10))

# Calculate Z values for the provided regression plane
z_surf_provided = -0.55519704 * x_surf + 9.07931034 * y_surf - 11.06206896551722

# Calculate Z values for the fitted regression plane
z_surf_fitted = intercept + coef_downlink * x_surf + coef_checks * y_surf

# Plot the provided regression plane
ax.plot_surface(x_surf, y_surf, z_surf_provided, color='orange', alpha=0.5, rstride=100, cstride=100, label='Provided Plane')

# Plot the fitted regression plane
ax.plot_surface(x_surf, y_surf, z_surf_fitted, color='green', alpha=0.5, rstride=100, cstride=100, label='Fitted Plane')

# Plot the user-provided point if requested
if user_point_plotted:
    ax.scatter(downlink_period_input, checks_input, difference_predicted, color='turquoise', s=100, label='Input Point')

# Set z-axis limits
ax.set_zlim(0, 100)

# Labels and title
ax.set_xlabel('Downlink Period')
ax.set_ylabel('Checks')
ax.set_zlabel('Difference (mA)')
plt.title("Power Budget Regression Planes, Summmer and Fall 2024")

# Custom legend
scatter_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='F24 Data Points')
scatter_legend2 = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='SU24 Data Points')
fitted_legend = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='green', markersize=10, label='Fitted Plane')

# Add user point legend if plotted
if user_point_plotted:
    user_point_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='turquoise', markersize=10, label='Input Point')
    ax.legend(handles=[scatter_legend, scatter_legend2, fitted_legend, user_point_legend])
else:
    ax.legend(handles=[scatter_legend, scatter_legend2, fitted_legend])

plt.show()
