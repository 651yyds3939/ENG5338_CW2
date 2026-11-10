# Member-reported analysis — received 10 November 2026

Historical author text retained for attribution. Current integrated findings are in the master notebook.

## Your analysis and contribution

**Write your analysis here, in this existing Markdown/text cell.** Double-click
this cell, replace the placeholders below with your own text, then press
`Shift + Enter` to render it. Save the notebook with your code, outputs and analysis.
This is a text cell, not a code cell.

- Name / student ID:Jiaqi Chen/[ID retained in original submission]
- What you actually implemented or changed: Based on Wenyi's shared code, I performed multiple rounds of hyperparameter tuning for the random forest model that predicts CO concentration. After selecting the best parameters, I refit the model with the fixed parameters for each fold and combined the actual and predicted values in a single scatter plot to investigate the model's issues.
- Why this model and these settings: I chose a random forest because it can capture nonlinear relationships between turbine operating conditions and CO concentration, as well as interactions among the operating variables. I selected the hyperparameter combination with the lowest mean validation MAE across the five time-series folds. Since adding more trees yielded only small improvements in the later trials, I fixed the number of trees at 600 for the final round of tuning.
- Training versus validation evidence: The best random forest configuration used 600 trees, a maximum depth of 11, a minimum of 20 samples per leaf, max_features=0.5, and max_samples=0.90. Across the five time-series validation folds, it achieved a mean validation MAE of 0.7371 (standard deviation 0.0857), compared with a mean training MAE of 0.4140. The gap of 0.3232 shows that prediction errors were higher on the later validation data. The mean validation RMSE was 1.5079, and the mean validation R² was 0.5767. On average, 81.16% of validation predictions were within ±1 of the measured CO value, below the group’s provisional target of 90%
- Temporal limitations / parameter boundaries / next steps: The above indicators are based on development data from 2011–2013. The data from 2014–2015 are reserved for the team to conduct final testing.I found that the model tends to underestimate CO at higher concentrations. My next step is to investigate how to reduce this bias.
- AI tools used and what for:I used ChatGPT to help write the code and to organise and refine the wording of the report.

Replace placeholders with your actual work and evidence. Do not invent results.
