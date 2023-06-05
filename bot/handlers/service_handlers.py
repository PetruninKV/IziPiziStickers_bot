from aiogram import Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated

from database.users import active_users
from config_data.config import config
from services.redis import RedisDB

router = Router()

redis_users: RedisDB = RedisDB(
    db=config.redis.users_db_id,
    decode_responses=True,
)


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    active_users.discard(event.from_user.id)
    print('Заблокировал')
    async with redis_users:
        await redis_users.rm_users_from_db('active_users', str(event.from_user.id))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    active_users.add(event.from_user.id)
    print('Разблокировал')
    async with redis_users:
        await redis_users.set_users_to_db('active_users', str(event.from_user.id))
