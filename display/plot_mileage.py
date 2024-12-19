import matplotlib.pyplot as plt
import pandas as pd

from data_load.activities import load_activities

def plot_mileage(mpw=False):
    activities = load_activities()
    activities['History Days'] = (activities['Activity Date'] - activities['Activity Date'].min()).dt.days
    activities['Cumulative Mileage'] = activities['Distance'].cumsum()
    activities['Activity Date Days'] = activities['Activity Date'].dt.date
    daily = activities.groupby('Activity Date Days')['Distance'].sum().reset_index()
    
    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=100)
    plt.plot(daily['Activity Date Days'], daily['Distance'], marker='o', label='Daily')
    if mpw:
        plt.plot(activities['Activity Date'], 7*activities['Cumulative Mileage (7D)']/7, marker='o', label='7 Day')
        plt.plot(activities['Activity Date'], 7*activities['Cumulative Mileage (30D)']/30, marker='o', label='30 Day')
        plt.plot(activities['Activity Date'], 7*activities['Cumulative Mileage (365D)']/365, marker='o', label='365 Day')
        plt.plot(activities['Activity Date'], 7*activities['Cumulative Mileage'] / activities['History Days'], marker='o', label='Total')
    else:
        plt.plot(activities['Activity Date'], activities['Cumulative Mileage (7D)']/7, marker='o', label='7 Day')
        plt.plot(activities['Activity Date'], activities['Cumulative Mileage (30D)']/30, marker='o', label='30 Day')
        plt.plot(activities['Activity Date'], activities['Cumulative Mileage (365D)']/365, marker='o', label='365 Day')
        plt.plot(activities['Activity Date'], activities['Cumulative Mileage'] / activities['History Days'], marker='o', label='Total')
    plt.xlabel('Date')
    if mpw:
        plt.ylabel('Miles Per Week')
        plt.title('Cumulative Miles Per Week Averages')
    else:
        plt.ylabel('Miles Per Day')
        plt.title('Rolling Window Mileage Averages')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    
    return plt.gca()

def plot_vdot():
    activities = load_activities()
    
    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=100)
    plt.plot(activities['Activity Date'], activities['VDOT Effective'], marker='o', label='Effective VDOT')
    plt.xlabel('Date')
    plt.ylabel('VDOT')
    plt.title('Effective VDOT Over Time')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.ylim([0, 80])
    
    return plt.gca()

if __name__ == "__main__":
    ax = plot_mileage(mpw=True)
    plt.sca(ax)
    plt.savefig('plots/weekly_mileage.png')
    ax = plot_mileage(mpw=False)
    plt.sca(ax)
    plt.savefig('plots/daily_mileage.png')
    ax = plot_vdot()
    plt.sca(ax)
    plt.savefig('plots/vdot.png')
    plt.show()