from aiogram import Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated

from database.users import active_users
from services.redis import RedisDB

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, redis_session: RedisDB):
    active_users.discard(event.from_user.id)
    print('Заблокировал')
    await redis_session.rm_users_from_db('active_users', str(event.from_user.id))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated, redis_session: RedisDB):
    active_users.add(event.from_user.id)
    print('Разблокировал')
    await redis_session.set_users_to_db('active_users', str(event.from_user.id))
