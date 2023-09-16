import vk_api
from jproperties import Properties
import sqlite3

# TODO add token
token = ""

con = sqlite3.connect("predictor.db")
cursor = con.cursor()

configs = Properties()
with open('credentials', 'rb') as config_file:
    configs.load(config_file)

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

def contains_href(text: str) -> bool:
    return '://' in text


def filter_posts(text: str) -> bool:
    contains_href(text)

def fetch_posts(group_id, label):
    for offset in range(0, 5000, 100):
        response = vk.wall.get(owner_id=group_id, offset=offset, count=100)
        response_posts = [post['text'] for post in response['items'] if not contains_href(post['text'])]
        if not response_posts: break
        for post in response_posts:
            cursor.execute("insert into posts (text, label) values(?, ?)", (post, label))
        con.commit()
        print(f"label: {label}, progress: {offset / 5000}")


if __name__ == '__main__':
    cooking_id = -42025607
    fashion_id = -59245439
    animal_id = -82267971
    cur = cursor.execute("SELECT text, class from test_posts")
    #cursor.execute("CREATE TABLE posts (text, label)")
    fetch_posts(cooking_id, 0)
    fetch_posts(fashion_id, 1)
    fetch_posts(animal_id, 2)