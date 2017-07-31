from .Listening.caption_util import *

# IMG_URL: 유튜브의 썸네일을 가져오는 URL
# VOD_URL1: 최근 시청한 비디오와 유사한 비디오를 가져오는 URL
# VOD_URL2: 일반적인 유튜브 검색처럼 검색어로 비디오를 가져오는 URL


# Parameter
# ->video_id: 연관된 유사 비디오를 찾기위한 비디오 id
# ->video_name: 검색하여 비디오를 찾을때 쓸 검색어
# ->max_results: 검색결과의 개수
# Return
# ->(url, 제목, 설명, 썸네일 url)
