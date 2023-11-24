from fastapi import FastAPI, APIRouter, HTTPException
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = APIRouter(
    prefix='/predictions',  # Set the prefix to 'matches'
    tags=['predictions']
)
templates = Jinja2Templates(directory='templates')
# Load the model and required data
matches = pd.read_csv("utils/all_matches.csv", index_col=0)
matches["date"] = pd.to_datetime(matches["date"])

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
train = matches[(matches["date"] < '2022-08-08')]
test = matches[matches["date"] > '2022-08-08']

# Define predictors
predictors = ["venue_code", "opp_code", "hour", "day_code"]

# Fit RandomForestClassifier
rf.fit(train[predictors], train["target"])

# Make predictions on the test set
preds = rf.predict(test[predictors])

# Calculate accuracy
acc = accuracy_score(test["target"], preds)

# Create a DataFrame for combined actual and predicted valuesz
combined = pd.DataFrame(dict(actual=test["target"], prediction=preds))

# Create a cross-tabulation
cross_tab = pd.crosstab(index=combined["actual"], columns=combined["prediction"])

# Calculate precision score
precision = precision_score(test["target"], preds)

# Group matches by 'team' column
grouped_matches = matches.groupby("team")


# Define a function for calculating rolling averages
def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(5, closed="left").mean()
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
    train = data[(data["date"] > '2020-01-01') & (data["date"] < '2024-08-08')]
    test = data[data["date"] > '2020-08-08']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], prediction=preds), index=test.index)
    precision = precision_score(test["target"], preds)
    return combined, precision


# Make predictions using rolling_matches data
combined, precision = make_predictions(rolling_matches, predictors + new_cols)

# Merge dataframes to include additional columns
combined = combined.merge(rolling_matches[["date", "team", "opponent", "result"]], left_index=True, right_index=True)
merged = combined.merge(combined, left_on=["date", "team"], right_on=["date", "opponent"])


def predict_winner(team1, team2):
    # Prepare features for the prediction
    team1_data = rolling_matches[rolling_matches["team"] == team1]
    team2_data = rolling_matches[rolling_matches["team"] == team2]

    # Make predictions using the RandomForestClassifier model
    team1_combined, team1_precision = make_predictions(team1_data, predictors + new_cols)
    team2_combined, team2_precision = make_predictions(team2_data, predictors + new_cols)

    if team1_precision > team2_precision:
        return f"{team1} is predicted to win {team1_precision} & {team2_precision}"
    elif team2_precision > team1_precision:
        return f"{team2} is predicted to win {team1_precision} & {team2_precision}"
    else:
        return f"It's predicted to be a draw {team1_precision} & {team2_precision}"


@router.get("/predict_winner")
async def predict_winner_view(request: Request, team1: str, team2: str):
    if team1 not in matches['team'].unique() or team2 not in matches['team'].unique():
        raise HTTPException(status_code=400, detail="Invalid team name(s). Please provide valid team names.")

    # Get the predicted winner between the provided teams
    winner = predict_winner(team1, team2)
    return winner
