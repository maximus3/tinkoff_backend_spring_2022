from fastapi import APIRouter

from app.channel import main_channel
from app.schema import History

router = APIRouter(
    prefix='/history',
    tags=['history'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/main', response_model=History)
async def get_messages_history() -> History:
    history = await main_channel.get_history()
    return History(channel_id=main_channel.channel_id, history=history)
