import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score

# Read the CSV file
matches = pd.read_csv("all_matches.csv", index_col=0)

# Data Preprocessing
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
matches["day_code"] = matches["date"].dt.dayofweek
matches["target"] = (matches["result"] == "W").astype("int")

# Initialize RandomForestClassifier
rf = RandomForestClassifier(n_estimators=550, min_samples_split=45, random_state=1)

# Split data into train and test sets
train = matches[matches["date"] < '2023-01-01']
test = matches[matches["date"] > '2023-01-01']

# Define predictors
predictors = ["venue_code", "opp_code", "hour", "day_code"]

# Fit RandomForestClassifier
rf.fit(train[predictors], train["target"])

# Make predictions on the test set
preds = rf.predict(test[predictors])

# Calculate accuracy
acc = accuracy_score(test["target"], preds)
print("Accuracy:", acc)

# Create a DataFrame for combined actual and predicted values
combined = pd.DataFrame(dict(actual=test["target"], prediction=preds))

# Create a cross-tabulation
cross_tab = pd.crosstab(index=combined["actual"], columns=combined["prediction"])
print("Cross-tabulation:\n", cross_tab)

# Calculate precision score
precision = precision_score(test["target"], preds)
print("Precision:", precision)

# Group matches by 'team' column
grouped_matches = matches.groupby("team")

# Define a function for calculating rolling averages
def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed="left").mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

# Get matches for a specific team
cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]

# Calculate rolling averages for matches
rolling_matches = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
rolling_matches = rolling_matches.droplevel("team")
rolling_matches.index = range(rolling_matches.shape[0])

# Function to make predictions
def make_predictions(data, predictors):
    train = data[data["date"] < '2022-06-06']
    test = data[data["date"] > '2023-01-01']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], prediction=preds), index=test.index)
    precision = precision_score(test["target"], preds)
    return combined, precision

# Make predictions using rolling_matches data
combined, precision = make_predictions(rolling_matches, predictors + new_cols)

# Merge dataframes to include additional columns
combined = combined.merge(rolling_matches[["date", "team", "opponent", "result"]], left_index=True, right_index=True)

# Mapping team names
map_values = {
    "Brighton and Hove Albion": "Brighton",
    "Manchester United": "Manchester Utd",
    "Newcastle United": "Newcastle Utd",
    "Tottenham Hotspur": "Tottenham",
    "West Ham United": "West Ham",
    "Wolverhampton Wanderers": "Wolves"
}
mapping = {**map_values}

combined["new_team"] = combined["team"].map(mapping)
merged = combined.merge(combined, left_on=["date", "new_team"], right_on=["date", "opponent"])

# Further processing or analysis with 'merged' dataframe
