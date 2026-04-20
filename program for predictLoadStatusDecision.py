import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

def ml1():
    df = pd.read_excel('Input.xlsx')

    # Function to determine Load1 and Load2 status
    def set_load_status(pv_irradiance):
        if 400 < pv_irradiance < 700.00:
            return 'ON', 'OFF'
        elif pv_irradiance > 700.01:
            return 'ON', 'ON'
        else:
            return 'OFF', 'OFF'

    # Apply load status logic
    df[['Load1', 'Load2']] = df['PV_irradiance'].apply(lambda x: pd.Series(set_load_status(x)))
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

    # Extract features
    df['Hour'] = df['Datetime'].dt.hour
    df['Minute'] = df['Datetime'].dt.minute
    df['Day'] = df['Datetime'].dt.day
    df['DayOfWeek'] = df['Datetime'].dt.weekday
    df['Month'] = df['Datetime'].dt.month
    df['Prev_PV_irradiance'] = df['PV_irradiance'].shift(1)

    df.dropna(inplace=True)

    latest_date = df['Date'].max()
    next_day = pd.to_datetime(latest_date) + pd.Timedelta(days=1)

    # Define time slots (08:00 to 17:00 every 30 minutes)
    time_slots = [(h, m) for h in range(8, 18) for m in (0, 30)]

    predictions = []

    for hour, minute in time_slots:
        df_slot = df[(df['Hour'] == hour) & (df['Minute'] == minute)]

        if df_slot.shape[0] < 2:
            continue

        X = df_slot[['Day', 'DayOfWeek', 'Month', 'Prev_PV_Voltage']]
        y = df_slot['PV_Voltage']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 🔄 Using DecisionTreeRegressor instead of RandomForest
        model = DecisionTreeRegressor(random_state=42)
        model.fit(X_train, y_train)

        last_voltage = df_slot.iloc[-1]['PV_Voltage']

        input_data = pd.DataFrame({
            'Day': [next_day.day],
            'DayOfWeek': [next_day.weekday()],
            'Month': [next_day.month],
            'Prev_PV_irradiance': [last_irradiance]
        })

        predicted_irradiance = model.predict(input_data)[0]
        load1, load2 = set_load_status(predicted_irradiance)

        predictions.append({
            'Datetime': pd.Timestamp(next_day.year, next_day.month, next_day.day, hour, minute),
            'Hour': hour,
            'Minute': minute,
            'Day': next_day.day,
            'DayOfWeek': next_day.weekday(),
            'Month': next_day.month,
            'Prev_PV_irradiance': last_irradaance,
            'PV_irradiance': predicted_irradiance,
            'Load1': load1,
            'Load2': load2
        })

    result_df = pd.DataFrame(predictions)
    result_df['Date'] = result_df['Datetime'].dt.date
    result_df['Time'] = result_df['Datetime'].dt.time

    # Append predictions to original data
    df_updated = pd.concat([df, result_df], ignore_index=True)

    # Rearranging and saving
    df_updated = df_updated[['PV_irradiance', 'Load1', 'Load2', 'Datetime', 'Date', 'Time']]
    df_updated.to_excel('updated_data_test_decision.xlsx', index=False)

    # Convert to MATLAB-style output
    result_df['Load1'] = result_df['Load1'].map({'ON': 1, 'OFF': 0})
    result_df['Load2'] = result_df['Load2'].map({'ON': 1, 'OFF': 0})

    return result_df[['Load1', 'Load2']].values.tolist()

ml1()
