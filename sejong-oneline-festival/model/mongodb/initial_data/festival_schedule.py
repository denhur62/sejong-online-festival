"""축제 일정"""
from datetime import datetime
FESTIVAL_SCHEDULE = {
    'config_type': 'festival_schedule',
    'schedules': [
        {
            'day_title': "19 TUE",
            'events': [
                {
                    "start_time": datetime.strptime("2021-10-19 14:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time": datetime.strptime("2021-10-19 15:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "학생회관",
                    "contents": "톡톡톡 토크콘서트",
                },
                {
                    "start_time": datetime.strptime("2021-10-19 15:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time": datetime.strptime("2021-10-19 16:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "학생회관",
                    "contents": "천하제일 인공지능 대회",
                }
            ]
        },
        {
            'day_title': "20 WED",
            'events': [
                {
                    "start_time": datetime.strptime("2021-10-20 10:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-20 11:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장",
                    "contents": "ONLINE 랜드",
                },
                {
                    "start_time": datetime.strptime("2021-10-20 12:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-20 13:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "박물관 앞",
                    "contents": "카트라이더",
                },
                {
                    "start_time": datetime.strptime("2021-10-20 14:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-20 15:22:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "광개토관 컨벤션홀",
                    "contents": "문어게임",
                },
                {
                    "start_time": datetime.strptime("2021-10-20 16:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-20 17:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장 메인무대",
                    "contents": "복면가왕",
                },
                {
                    "start_time": datetime.strptime("2021-10-20 20:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-20 21:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장 메인무대",
                    "contents": "초청가수",
                },

            ]
        },
        {
            'day_title': "21 TUR ",
            'events': [
                {
                    "start_time": datetime.strptime("2021-10-21 13:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-21 14:14:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장",
                    "contents": "ONLINE 랜드",
                },
                {
                    "start_time": datetime.strptime("2021-10-21 15:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-21 16:14:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "박물관 앞",
                    "contents": "카트라이더",
                },
                {
                    "start_time": datetime.strptime("2021-10-21 16:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-21 17:14:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장 메인무대",
                    "contents": "초청가수",
                },
            ]
        },
        {
            'day_title': "22 FRI",
            'events': [
                {
                    "start_time": datetime.strptime("2021-10-22 13:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-22 16:14:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "박물관 앞",
                    "contents": "카트라이더",
                },
                {
                    "start_time": datetime.strptime("2021-10-22 14:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-22 15:14:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장 메인무대",
                    "contents": "창현 거래노래방",
                },
                {
                    "start_time": datetime.strptime("2021-10-22 17:21:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "end_time":datetime.strptime("2021-10-22 18:13:57.86", '%Y-%m-%d %H:%M:%S.%f'),
                    "place_info": "운동장 메인무대",
                    "contents": "초청가수",
                },
            ]
        },
    ]
}