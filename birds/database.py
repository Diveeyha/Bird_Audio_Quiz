import streamlit as st
import pandas as pd
import os


def get_csv_name(filename):
    csv_dir = os.path.dirname(__file__)
    return os.path.join(csv_dir, 'resources', filename)


# @st.cache_data
def load_csv(filename):
    csv = pd.read_csv(get_csv_name(filename))
    return csv.sort_values(by=csv.columns[0])


def save_csv(filename, dataframe):
    dataframe.to_csv(get_csv_name(filename), index=False)


@st.cache_data
def get_birds_by_group(csv, *groups):
    df = csv[csv['Group'].isin(*groups)]
    return df.sort_values(by=['Name'])


@st.cache_data
def get_birds_by_order(csv, *orders):
    df = csv[csv['Order'].isin(*orders)]
    return df.sort_values(by=['Name'])


@st.cache_data
def get_birds_by_family(csv, *families):
    df = csv[csv['Family'].isin(*families)]
    return df.sort_values(by=['Name'])


@st.cache_data
def get_birds_by_taxonomic_name(csv, *species):
    df = csv[csv['Name'].isin(*species)]
    return df.sort_values(by=['Name'])
