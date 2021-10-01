from datetime import datetime
CELEBRITY_LINEUP = {
    "config_type": "celebrity_lineup",
    "banner_photos":["/uploads/c1.png","/uploads/c2.png","/uploads/c3.png"],
    "celebrities": [
        {
            "name": "매드클라운",
            "datetime_info": "10.20 WED",
            "youtube_link":"https://www.youtube.com/watch?v=2fFaD2uIf30",
            "open_time": datetime.strptime("2021-10-19 14:21:57.86", "%Y-%m-%d %H:%M:%S.%f"),
        },
        {
            "name": "청하",
            "datetime_info": "10.21 TUR",
            "youtube_link":"https://www.youtube.com/watch?v=900X9fDFLc4",
            "open_time": datetime.strptime("2020-10-20 14:21:57.86", "%Y-%m-%d %H:%M:%S.%f"),
        },
        {
            "name": "장범준",
            "datetime_info": "10.21 TUR",
            "youtube_link":"https://www.youtube.com/watch?v=BfWqUjunXXU",
            "open_time": datetime.strptime("2021-10-20 14:21:57.86", "%Y-%m-%d %H:%M:%S.%f"),
        }
    ]
}
