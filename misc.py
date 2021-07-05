from setting import MONGO_DB
from bson import ObjectId

def _get_xxtx(to_user,from_user):
    to_user_info = MONGO_DB.toys.find_one({'_id':ObjectId(to_user)})

    for friend in to_user_info.get('friend_list'):
        # print(friend.get("friend_id"))
        # print(from_user)
        if friend.get("friend_id") == from_user:
            xxtx_str = f"您有来自{friend.get('friend_nick')}的新消息"
            break
    else:
        xxtx_str = "您有来自陌生人的新消息"

    return xxtx_str