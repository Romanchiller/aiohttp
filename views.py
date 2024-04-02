from aiohttp import web
from sqlalchemy import select
from auth import hash_password, check_password
from schema import Login, CreateAdvertisements, UpdateAdvertisements, CreateUser, UpdateUser
from tools import validate
from tools import get_http_error
from models import Session, Token, User, Advertisement, MODEL_TYPE
from sqlalchemy.exc import IntegrityError


async def get_item_by_id(session: Session, item_id: int, model: Advertisement | User):
    item = await session.get(model, item_id)
    if item is None:
        raise get_http_error(web.HTTPNotFound, f"Item with id {item_id} not found ")
    return item


async def add_item(session: Session, model: MODEL_TYPE):
    try:
        session.add(model)
        await session.commit()
    except IntegrityError as error:
        raise get_http_error(web.HTTPConflict, message="Item is already exists")
    return model

class BaseView(web.View):

    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def token(self) -> Token:
        return self.request.token

    @property
    def user(self) -> User:
        return self.request.token.user_id

    async def check_token(self):
        try:
            header_token = self.request.headers['Authorization']
        except KeyError:
            raise get_http_error(web.HTTPNonAuthoritativeInformation, 'Token not found')
        try:
            token = await self.session.execute(select(Token).where(Token.token == header_token))
        except sqlalchemy.exc.DBAPIError:
            raise get_http_error(web.HTTPUnauthorized, 'Invalid token')
        token = token.scalars().first()
        self.request.token = token
        return True

class LoginView(BaseView):
    async def post(self):
        payload = validate(Login, await self.request.json())
        user = await self.session.execute(select(User).where(User.name == payload['name']))
        result = user.scalars().first()
        if result is None:
            raise get_http_error(web.HTTPError, message="user not found")
        if check_password(payload["password"], result.password):
            token = Token(user_id=result.id)
            await add_item(self.session, token)
            return web.json_response(token.dict)
        else:
            raise get_http_error(web.HTTPUnauthorized, 'invalid password')


class UserView(BaseView):

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get_current_user(self):
        return await get_item_by_id(self.session, self.user_id, User)

    async def get(self):
        user = await self.get_current_user()
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        payload = validate(CreateUser, json_data)
        payload["password"] = hash_password(payload["password"])
        user = User(**payload)
        user = await add_item(self.session, user)
        return web.json_response({'id': user.id})


    async def patch(self):
        if await self.check_token():
            if self.token.user_id == int(self.request.match_info["user_id"]):
                json_data = await self.request.json()
                payload = validate(UpdateUser, json_data)
                user = await self.get_current_user()
                if "password" in json_data:
                    payload["password"] = hash_password(payload["password"])
                for field, value in json_data.items():
                    setattr(user, field, value)
                user = await add_item(self.session, user)
                return web.json_response(user.dict)
            else:
                raise get_http_error(web.HTTPUnauthorized, 'Not your user')


    async def delete(self):
        if await self.check_token():
            if self.token.user_id == int(self.request.match_info["user_id"]):
                user = await self.get_current_user()
                await self.session.delete(user)
                await self.session.commit()
                return web.json_response({'status': 'deleted'})
            else:
                raise get_http_error(web.HTTPUnauthorized, 'Not your user')


class AdvertisementView(BaseView):

    @property
    def adv_id(self):
        return int(self.request.match_info["adv_id"])

    async def get_current_adv(self):
        return await get_item_by_id(self.session, self.adv_id, Advertisement)

    async def check_owner(self):
        token_author = self.user
        print(token_author)
        adv = await self.get_current_adv()
        print(adv.author_id)
        if token_author == adv.author_id:
            return adv
        else:
            raise get_http_error(web.HTTPUnauthorized, 'not your adv')


    async def get(self):
        adv = await self.get_current_adv()
        return web.json_response(adv.dict)

    async def post(self):
        json_data = await self.request.json()
        payload = validate(CreateAdvertisements, json_data)
        if await self.check_token():
            if self.token:
                payload['author_id'] = self.token.user_id
                adv = Advertisement(**payload)
                adv = await add_item(self.session, adv)
                return web.json_response(adv.dict)
            else:
                raise get_http_error(web.HTTPNotFound, 'user not exist')


    async def patch(self):
        json_data = await self.request.json()
        payload = validate(UpdateAdvertisements, json_data)
        if await self.check_token():
            adv = await self.check_owner()
            for field, value in payload.items():
                setattr(adv, field, value)
            adv = await add_item(self.session, adv)
            return web.json_response(adv.dict)


    async def delete(self):
        if await self.check_token():
            adv = await self.check_owner()

            await self.session.delete(adv)
            await self.session.commit()
            return web.json_response({'status': 'deleted'})
