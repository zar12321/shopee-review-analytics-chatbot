def preprocess_reviews(df):
    import pandas as pd
    from unidecode import unidecode
    import re
    df_clean = df.copy()

    def clean_text(text):
        text = str(text)
        text = unidecode(text)
        text = re.sub(r"\s+", " ", text) # menghapus spasi berlebih
        text = text.strip() # menghapus spasi di awal dan akhir
        return text

    df_clean["content"] = df_clean["content"].apply(clean_text)

    # menghapus duplikasi data
    df_clean.drop_duplicates(
        subset = ["content"],
        inplace = True # mengubah dataframe secara langsung
    )

    # menghapus review yang terlalu pendek
    df_clean = df_clean[
        df_clean["content"].str.len() > 10
    ]

    # mereset index
    df_clean.reset_index(
        drop = True,
        inplace = True
    )

    # mengganti NaT menjadi None pada kolom repliedAt
    df_clean["repliedAt"] = df_clean["repliedAt"].astype(object)
    df_clean["repliedAt"] = df_clean["repliedAt"].where(
        pd.notnull(df_clean["repliedAt"]),
        None
    )

    # menangani jika terdapat replyContent yang kosong
    df_clean["replyContent"] = df_clean["replyContent"].where(
        pd.notnull(df_clean["replyContent"]),
        None
    )

    return df_clean 