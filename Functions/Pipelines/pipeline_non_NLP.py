
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from numpy import argsort
from Functions.AlertP1.data_cleaning import *
from Functions.AlertP1.features import *
from Functions.analysis.step_analysis import *
from Functions.AlertP1.dummy_features import *
from Functions.Models.evaluation import *
from Functions.NLP.data_with_nlp import *

def pre_process(df):
    #Additional Functions

    def sort_values(df):
        df = df.sort_values('DATA_RECEPCAO')
        return df
    def text_only(df):
        df=df[df['text_length']>0]
        return df

   

    #Pipeline

    pipeline = Pipeline([
        #Data Cleaning
        ('Date Format', FunctionTransformer(date_format_alertP1)),
        ('Replace Blanks', FunctionTransformer(replace_blank)),
        ('Duplicated Entities', FunctionTransformer(entity_duplicated)),
        ('Target Variable', FunctionTransformer(result)),
        #Structured Features
        ('Accepted Before', FunctionTransformer(bef_accepted)),
        ('Area Classification', FunctionTransformer(class_area)),
        ('Text Length', FunctionTransformer(text_length)),
        ('Referral Steps', FunctionTransformer(referral_steps)),
        ('Speciality', FunctionTransformer(speciality)),
        ('Unit', FunctionTransformer(unit)),
        ('Lower Case Text ', FunctionTransformer(lowering_text)),
        ('clean_text', FunctionTransformer(clean_text)),
        #Dummies
        ('Dummies', FunctionTransformer(structured_data_dummies)),
        #Keep only text rows
        ('Text Only', FunctionTransformer(text_only)),
        #Sort Values
        ('Sort Values', FunctionTransformer(sort_values))
    ])
    transformed_data = pipeline.fit_transform(df)

    return transformed_data