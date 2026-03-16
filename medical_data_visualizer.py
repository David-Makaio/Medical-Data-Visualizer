import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('medical_examination.csv')

bmi = df['weight']/ ((df['height']/100) ** 2)
df['overweight'] = (bmi > 25).astype(int)

df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


def draw_cat_plot():
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    fig = sns.catplot(
        x='variable', 
        hue='value', 
        col='cardio', 
        data=df_cat, 
        kind='count', 
        order=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    )
    fig.set_axis_labels("variable", "total")

    fig.savefig('catplot.png')
    return fig.fig


def draw_heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    corr = df_heat.corr()

    mask = np.triu(corr)

    fig, ax = plt.subplots(figsize=(12, 12))

    sns.heatmap(
        corr, mask=mask, annot=True, fmt='.1f', 
        center=0, square=True, linewidths=.5, 
        cbar_kws={'shrink': .5}
    )

    fig.savefig('heatmap.png')
    return fig