import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import time


data=pd.read_json('data.json')
data = data['close'].tolist()


#Step 2: Create Moving Windows
def create_moving_windows(data, window_size, step_size):
    windows = []
    for start in range(0, len(data) - window_size + 1, step_size):
        end = start + window_size
        windows.append(data[start:end])
    return windows

window_size = 30  # size of each window
step_size = 10     # step size for moving the window
windows = create_moving_windows(data, window_size, step_size)


#Step 3: Calculate Drift for Each Window

def detect_drift(reference_window, current_window):
    ks_statistic, p_value = ks_2samp(reference_window, current_window)
    return ks_statistic, p_value

reference_window = windows[0]
drift_results = []

for i, window in enumerate(windows[1:], start=1):
    ks_statistic, p_value = detect_drift(reference_window, window)
    drift_results.append((i, ks_statistic, p_value))


#Step 4: Evaluate and Interpret Results
# drift_threshold = 0.05

# for i, ks_statistic, p_value in drift_results:
#     if p_value < drift_threshold:
#         print(f"Drift detected in window {i} with KS statistic {ks_statistic:.3f} and p-value {p_value:.3f}")
#     else:
#         print(f"No significant drift in window {i} with KS statistic {ks_statistic:.3f} and p-value {p_value:.3f}")



#Step 5: Automate for Streaming Data

def monitor_streaming_data(new_data_generator, window_size, step_size, reference_window, drift_threshold=0.05):
    current_data = []
    
    for new_data in new_data_generator:
        current_data.extend(new_data)
        if len(current_data) >= window_size:
            windows = create_moving_windows(current_data, window_size, step_size)
            current_window = windows[-1]
            ks_statistic, p_value = detect_drift(reference_window, current_window)
            if p_value < drift_threshold:
                print(f"Drift detected with KS statistic {ks_statistic:.3f} and p-value {p_value:.3f}")
                reference_window = current_window  # Update reference window if drift detected
            current_data = current_data[step_size:]  # Slide window
            
            time.sleep(1)  # Simulate waiting for new data

# Example new data generator (replace with real data source)
def new_data_generator():
    while True:
        yield np.random.randn(100)  # Generate new data

monitor_streaming_data(new_data_generator(), window_size, step_size, reference_window)
