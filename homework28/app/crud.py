from typing import Optional
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models import Item, ItemCreate, ItemUpdate


async def create_item(session: AsyncSession, item_data: ItemCreate) -> Item:
    """Створює новий елемент у базі даних"""

    item = Item.model_validate(item_data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def get_item(session: AsyncSession, item_id: int) -> Optional[Item]:
    """Повертає елемент за його ідентифікатором"""

    return await session.get(Item, item_id)


async def get_items(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        owner_id: Optional[int] = None,
        search: Optional[str] = None,
        sort_by: str = "id",
        sort_order: str = "asc"
) -> list[Item]:
    """Повертає список елементів із фільтрацією, пошуком і сортуванням"""

    statement = select(Item)

    if owner_id is not None:
        statement = statement.where(Item.owner_id == owner_id)

    if search:
        statement = statement.where(Item.title.contains(search))

    sort_columns = {
        "id": Item.id,
        "title": Item.title,
        "price": Item.price,
        "owner_id": Item.owner_id,
        "is_active": Item.is_active
    }

    sort_column = sort_columns.get(sort_by, Item.id)

    if sort_order == "desc":
        statement = statement.order_by(desc(sort_column))
    else:
        statement = statement.order_by(asc(sort_column))

    statement = statement.offset(skip).limit(limit)

    result = await session.execute(statement)
    return list(result.scalars().all())


async def update_item(
        session: AsyncSession,
        item_id: int,
        item_data: ItemUpdate,
        owner_id: int
) -> Optional[Item]:
    """Оновлює елемент, якщо власник має доступ"""

    item = await session.get(Item, item_id)

    if not item:
        return None

    if item.owner_id != owner_id:
        return False

    item_data_dict = item_data.model_dump(exclude_unset=True)

    for key, value in item_data_dict.items():
        setattr(item, key, value)

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return item


async def delete_item(session: AsyncSession, item_id: int, owner_id: int) -> Optional[bool]:
    """Видаляє елемент, якщо власник має доступ"""

    item = await session.get(Item, item_id)

    if not item:
        return None

    if item.owner_id != owner_id:
        return False

    await session.delete(item)
    await session.commit()

    return True
