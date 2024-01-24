import requests
import requests
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

app = FastAPI()


def get_engagement_rate(username: str):
    try:
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"

        payload = {}
        headers = {
            'x-ig-app-id': '936619743392459',
            'Cookie': 'csrftoken=IAJUKUAGWTtjJo5s-aWSKP; ig_did=FA331715-D799-4F85-A97E-4D0E4053BC9F; ig_nrcb=1; mid=ZbC72AAEAAHAYvWx9IQKZTqBfSPH'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()
        list_post = data.get(
            "data")['user']['edge_owner_to_timeline_media']['edges']
        followers = data.get("data")['user']['edge_followed_by']['count']
        total_like = 0
        total_comment = 0
        for item in list_post:
            total_like += item['node']['edge_liked_by']['count']
            total_comment += item['node']['edge_media_to_comment']['count']
        avg_like = total_like / len(list_post)
        avg_comment = total_comment / len(list_post)
        engage = avg_like + avg_comment
        engage_rate = (engage / followers) * 100
        return {
            "username": username,
            "total_followers": followers,
            "total_like": total_like,
            "total_comment": total_comment,
            "avg_like": avg_like,
            "avg_comment": avg_comment,
            "engage_rate": engage_rate
        }
    except:
        raise HTTPException(status_code=404, detail="User not found")


@app.get("/engage_rate")
def get_engage(username: str):
    return get_engagement_rate(username)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
