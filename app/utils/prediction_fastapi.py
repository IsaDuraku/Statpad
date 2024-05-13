import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score

def preprocess_data(matches):
    matches["date"] = pd.to_datetime(matches["date"])
    matches["venue_code"] = matches["venue"].astype("category").cat.codes
    matches["opp_code"] = matches["opponent"].astype("category").cat.codes
    matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
    matches["day_code"] = matches["date"].dt.dayofweek
    matches["target"] = (matches["result"] == "W").astype("int")
    return matches

def train_rf_model(matches, predictors):
    rf = RandomForestClassifier(n_estimators=550, min_samples_split=45, random_state=1)
    train = matches[matches["date"] < '2023-11-11']
    rf.fit(train[predictors], train["target"])
    return rf

def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(10, closed="left").mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

def prepare_rolling_matches(matches):
    cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
    new_cols = [f"{c}_rolling" for c in cols]
    rolling_matches = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))
    rolling_matches = rolling_matches.droplevel("team")
    rolling_matches.index = range(rolling_matches.shape[0])
    return rolling_matches

def make_predictions(rf,data, predictors):
    train = data[data["date"] < '2023-01-01']
    test = data[data["date"] > '2023-01-01']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], prediction=preds), index=test.index)
    precision = precision_score(test["target"], preds)
    return combined, precision

def predict_winner_between_teams(team1, team2, predictors, rolling_matches, new_cols):
    team1_data = rolling_matches[rolling_matches["team"] == team1]
    team2_data = rolling_matches[rolling_matches["team"] == team2]

    if team1_data.empty or team2_data.empty:
        return "Insufficient data for prediction"

    team1_combined, team1_precision = make_predictions(team1_data, predictors + new_cols)
    team2_combined, team2_precision = make_predictions(team2_data, predictors + new_cols)

    if team1_precision > team2_precision:
        return f"{team1} is predicted to win against {team2}"
    elif team2_precision > team1_precision:
        return f"{team2} is predicted to win against {team1}"
    else:
        return "It's predicted to be a draw"

# Load data
matches = pd.read_csv("all_matches.csv", index_col=0)
matches = preprocess_data(matches)

# Define predictors
predictors = ["venue_code", "opp_code", "hour", "day_code"]

# Train RandomForestClassifier model
rf_model = train_rf_model(matches, predictors)

# Prepare rolling averages
rolling_matches = prepare_rolling_matches(matches)

# Make predictions
team1 = "Aston Villa"  # Replace with the first team name
team2 = "Burnley"  # Replace with the second team name

prediction = predict_winner_between_teams(team1, team2, rf_model, predictors, rolling_matches)
print(prediction)