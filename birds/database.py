import streamlit as st
import pandas as pd
import os


def get_csv_name():
    csv_dir = os.path.dirname(__file__)
    return os.path.join(csv_dir, 'resources', 'database.csv')


@st.cache_data
def load_csv():
    csv = pd.read_csv(get_csv_name())
    return csv.sort_values(by=csv.columns[0])


def save_csv(dataframe, index=True):
    dataframe.to_csv(get_csv_name(), index=index)


@st.cache_data
def get_birds_by_group(*groups):
    csv = load_csv()
    df = csv[csv['group'].isin(groups)]
    return df.sort_values(by=['name'])


@st.cache_data
def get_birds_by_order(*orders):
    csv = load_csv()
    df = csv[csv['order'].isin(orders)]
    return df.sort_values(by=['name'])


@st.cache_data
def get_birds_by_family(*families):
    csv = load_csv()
    df = csv[csv['family'].isin(families)]
    return df.sort_values(by=['name'])


@st.cache_data
def get_birds_by_taxonomy(*species):
    csv = load_csv()
    df = csv[csv['species'].isin(species)]
    return df.sort_values(by=['name'])
