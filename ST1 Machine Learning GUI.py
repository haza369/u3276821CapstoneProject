import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class TeslaStockPricePredictionApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Tesla Stock Close Predictor')
        self.data = pd.read_csv('TESLA.csv') 
        keep_columns = ['High', 'Low', 'Close'] 
        self.data = self.data[keep_columns] 

        self.sliders = []
                
        self.X = self.data.drop('Close', axis=1).values
        self.Y = self.data['Close'].values 
        
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.3, random_state=428)

        self.model = LinearRegression()
        self.model.fit(self.X_train, self.Y_train)

        self.create_widgets()

    def create_widgets(self):
        for i, column in enumerate(self.data.columns[:-1]):
            label = tk.Label(self.master, text=column + ': ')
            label.grid(row=i, column=0)
            current_val_label = tk.Label(self.master, text='0.0')
            current_val_label.grid(row=i, column=2)
            slider = ttk.Scale(self.master, from_=self.data[column].min(), to=self.data[column].max(), orient="horizontal",command=lambda val, label=current_val_label: label.config(text=f'{float(val):.2f}'))
            slider.grid(row=i, column=1)
            self.sliders.append((slider, current_val_label))

        predict_button = tk.Button(self.master, text='Predict Close', command=self.predict_price)
        predict_button.grid(row=len(self.data.columns[:-1]), columnspan=3)

    def predict_price(self):
        inputs = [float(slider.get()) for slider, _ in self.sliders]
        price = self.model.predict([inputs])
        messagebox.showinfo('Predicted Close', f'The predicted stock Close price is ${price[0]:.2f}')

if __name__ == '__main__':
    root = tk.Tk()
    app = TeslaStockPricePredictionApp(root)
    root.mainloop()