from aiogram import Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated

from database.users import active_users

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    active_users.discard(event.from_user.id)
    print('Заблокировал')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    active_users.add(event.from_user.id)
    print('Разблокировал')
