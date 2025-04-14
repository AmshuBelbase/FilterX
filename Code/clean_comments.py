import pandas as pd
import re

df = pd.read_csv('post_data/combined_csv.csv', header=None, names=[
    "post_shortcode", "commenter_profile", "comment_text", "comment_likes"
])


def remove_emojis(text):
    if isinstance(text, str):
        # This regex finds patterns like :face_with_tears_of_joy:
        return re.sub(r':[a-zA-Z0-9_]+:', '', text)
    return text


df['comment_text'] = df['comment_text'].apply(remove_emojis)

df.to_csv('post_data/combined_csv.csv', index=False)

print("Emojis removed and data saved to 'combined_csv.csv'.")
