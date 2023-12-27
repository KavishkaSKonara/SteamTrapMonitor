import tkinter as tk
import tkinter as tk
from matplotlib.figure import Figure
import numpy as np
import threading
import queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time
import queue
import random
import serial
import numpy as np
import joblib
import pandas as pd
loaded_model = joblib.load('logistic_regression_model.pkl', mmap_mode=None)

# Define the serial port and baud rate
ser = serial.Serial('COM7', 9600)
dt=0.1
plots=0
x_value1 = 0.0
x_value2 = 5
probability=0.76
steem_status ="Good"
x=0
y=0
z=0
xx=0
yy=0
zz=0
num_steps = 50
valx = np.zeros(num_steps)
valy = np.zeros(num_steps)
valz = np.zeros(num_steps)


# Number of lines to read
num_lines = 200

# Initialize an empty list to store the data
data_list = []
def calk():
    global plots,xx,yy,zz
    while(1):
        time.sleep(0.01)
        if(plots==1):

            probability_label.config(text=f"Probability : Testing")
            status_label.config(text=f"Steem tap satatus : Testing")
            try:
                for _ in range(num_lines):
                    time.sleep(0.01)
                    # Read a line from the serial port
                    serial_data = ser.readline().decode('utf-8', 'ignore').strip()

                    try:
                        # Split the data into a list of floats
                        data_values = [float(value) for value in serial_data.split()]
                        xx,yy,zz = [float(value) for value in serial_data.split()]
                        print(xx,yy,zz)

                        # Append the list of values to the data_list
                        data_list.append(data_values)

                        # Print the received data
                        print("Received data:", data_values)

                    except ValueError as e:
                        # Handle the case where conversion to float fails
                        print(f"Error converting data: {e}. Skipping line: {serial_data}")

            except KeyboardInterrupt:
                # Close the serial port when the script is interrupted
                ser.close()
                print("Serial port closed.")

            # Convert the list of lists to a NumPy array
            all_datasets = np.array(data_list)

            # Initialize arrays to store predictions and probabilities
            predictions = []
            probabilities = []

            for i, single_dataset in enumerate(all_datasets):
                data = np.array(single_dataset).reshape(1, -1)
                dataframe = pd.DataFrame(data, columns=['X', 'Y', 'Z'])

                y_pred_n = loaded_model.predict(dataframe)
                y_pred_prob = loaded_model.predict_proba(dataframe)[:, 1]

                # Append predictions and probabilities to arrays
                predictions.append("Bad" if (y_pred_n == 0).any() else "Good")
                probabilities.append(y_pred_prob)

            # print(f"Prediction for Dataset {i + 1}: Steem Trap Status:{predictions[-1]} -> Probability {y_pred_prob}")

            # Compare overall counts of "Good" and "Bad" predictions
            overall_good_count = predictions.count("Good")
            overall_bad_count = predictions.count("Bad")

            # Determine overall result based on counts
            overall_result = "Good" if overall_good_count > overall_bad_count else "Bad"

            # Calculate overall probability as the average of individual probabilities
            overall_probability = np.mean(probabilities)

            print(f"\nOverall Results:")

            print(f"Steam Trap status : {overall_result}")
            print(f"Probability: {overall_probability}")
            probability=overall_probability
            steem_status=overall_result

            plots=0

            probability_label.config(text=f"Probability : {probability} %")
            status_label.config(text=f"Steam Trap Status : {steem_status}")


def start():
    global plots
    plots = 1



def cal():
    global xx,yy,zz

    o= random.randint(1, 100)

    return xx,yy,zz

def plotx(start_time,end_time):
    global valx,valy,z,x,y,z
    diff = end_time - start_time
    end = int(diff / dt)
    for step in range(0, end):
        time.sleep(0.001)
        valx[step],valy[step],valz[step], = cal()


    x = np.arange(start_time, end_time, dt)
    plot1.clear()
    plot1.plot(x, valx, label='X')
    plot1.plot(x, valy, label='Y')
    plot1.plot(x, valz, label='Z')
    plot1.grid(True, linestyle='--', alpha=0.7)
    plot1.set_xlabel('Time')
    plot1.set_ylabel('V(mv)')
    plot1.legend()
def update_plot(frame):
    global x_value1, x_value2
    plotx(x_value1,x_value2)

    x_value1 += 0.1
    x_value2 += 0.1

    # Put the updated plot in the queue for the GUI thread to consume

    update_queue.put(fig)

def animate():
    global plots
    while(1):
       time.sleep(0.01)
       if(plots==1):
         update_plot(None)
         updated_fig = update_queue.get()
         canvas_n1.draw()






root = tk.Tk()
root.title("Steam trap")
root.geometry("700x500+300+150")
root.overrideredirect(False)
root.configure(bg="darkolivegreen2")

title_bar = tk.Frame(root, bg="darkorange", height=50)  # Change "lightblue" to your desired color
title_bar.pack(fill="x")

title_label = tk.Label(root, text="Steam Trap Checker", bg="darkorange", fg="white", font=("Helvetica", 25, "bold"))
title_label.place(x=10, y=4)


#device sttus
device_label = tk.Label(root, text="Device :", bg="darkolivegreen2", fg="black", font=("Helvetica", 10) )
device_label.place(x=10, y=90)

device_label = tk.Label(root, text="E17169 :", bg="darkolivegreen2", fg="blue", font=("Helvetica", 10) )
device_label.place(x=70, y=90)

devices_label = tk.Label(root, text="Status :", bg="darkolivegreen2", fg="black", font=("Helvetica", 10) )
devices_label.place(x=10, y=120)

devices_label = tk.Label(root, text="Connceted ", bg="darkolivegreen2", fg="blue", font=("Helvetica", 10) )

devices_label.place(x=70, y=120)
#buttons

button_tab1 = tk.Button(root, text="Start Test", command=start, bg="red", fg="white", font=("Arial", 12, "bold"),width=7, height=1,relief="flat")
button_tab1.place(x=30, y=200)

button_tab1.bind("<Enter>", lambda event: button_tab1.config(bg="deeppink1",fg="white"))
button_tab1.bind("<Leave>", lambda event: button_tab1.config(bg="red"))


#results frame
frame_results = tk.Frame(root, width=250, height=150, bg="ivory2")
frame_results.place(x=30, y=300)

title_label = tk.Label(frame_results, text="Results", bg="darkolivegreen", fg="white", font=("Helvetica", 15, "bold"), width=22)
title_label.place(x=0, y=0)

probability_label = tk.Label(frame_results, text="Probability : NA", bg="white", fg="darkslateblue", font=("Helvetica", 10) )
probability_label.place(x=10, y=50)
status_label = tk.Label(frame_results, text="Steam Trap Status : NA", bg="white", fg="darkslateblue", font=("Helvetica", 10) )
status_label.place(x=10, y=90)



#plot

fig = Figure(figsize=(4, 3), dpi=100)
plot1 = fig.add_subplot(1, 1, 1)
plot1.set_facecolor('black')


canvas_n1 = FigureCanvasTkAgg(fig, master=root)
canvas_n1.draw()
canvas_n1.get_tk_widget().place(x=290, y=100)


update_queue = queue.Queue()
animation_thread = threading.Thread(target=animate)
animation_thread.start()

callk_thread = threading.Thread(target=calk)
callk_thread.start()

root.mainloop()


