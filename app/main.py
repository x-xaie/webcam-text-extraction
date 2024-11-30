# app/main.py
from tkinter import Tk
from app.gui import App

def main():
    root = Tk()
    app = App(root)
    app.run()

if __name__ == "__main__":
    main()
