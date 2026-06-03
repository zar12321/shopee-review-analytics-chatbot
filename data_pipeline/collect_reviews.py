def collect_review():
    import pandas as pd
    from datetime import datetime
    from google_play_scraper import reviews, Sort

    app_id = "com.shopee.id"
    today = datetime.today()
    batas = datetime(today.year, today.month, 1) # untuk dapat review dari tanggal 1 bulan ini sampai sekarang

    # inisialisasi seluruh review
    all_reviews = []
    # penanda posisi terakhir data yang sudah diambil
    token = []

    while True:
        results, token = reviews(
            app_id,
            lang="id",
            country="id",
            sort = Sort.NEWEST,
            count = 200,
            continuation_token = token
        )

        if not results:
            break

        for review in results:
            if review["at"] < batas:
                break
            all_reviews.append(review)

        if results[-1]["at"] < batas:
            break

        print("Jumlah review: ", len(all_reviews))

        df = pd.DataFrame(all_reviews)
        print(df.columns.tolist())

        df = df[
            [
                "reviewId",
                "userName",
                "content",
                "score",
                "at",
                "replyContent",
                "repliedAt"
            ]
        ]
        df.head(5)

        df.to_csv("Review Shopee Bulan Mei 2026.csv", index=False)

        return df
    