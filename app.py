import gradio as gr
import pandas as pd
import joblib
from sklearn.metrics.pairwise import linear_kernel

model = joblib.load('episode2rec.pkl')

def recommend(input_text):
    matrix = model.fit_transform(df['Text'])
    key_terms_vector = model.transform(input_text)
    cosine_similarities = linear_kernel(key_terms_vector, matrix)
    similarity_df = pd.DataFrame({'Episode': df['Episode'], 'Similarity': cosine_similarities[0]})

    sorted_df = similarity_df.sort_values(by='Similarity', ascending=False)

    relevant_episodes = sorted_df[sorted_df['Similarity'] > 0]

    return relevant_episodes[['Episode']]

input_text = gr.Textbox(text="Enter your key terms/themes here (e.g. 'AI', 'female', 'reality')")
output_df = gr.Output(type='dataframe')

interface = gr.Interface(fn=recommend, inputs=input_text, outputs=output_df, title='Black Mirror Episode Recommender')

interface.launch()