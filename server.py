
from aiohttp import web
from models import Session, engine, init_db
from views import UserView, AdvertisementView, LoginView




app = web.Application()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def init_orm(app: web.Application):
    print("START")
    await init_db()
    yield
    await engine.dispose()
    print("FINISH")


app.middlewares.append(session_middleware)
app.cleanup_ctx.append(init_orm)


app.add_routes(
    [
        web.post("/user", UserView),
        web.get("/user/{user_id:\d+}", UserView),
        web.patch("/user/{user_id:\d+}", UserView),
        web.delete("/user/{user_id:\d+}", UserView),
        web.post("/adv", AdvertisementView),
        web.get("/adv/{adv_id:\d+}", AdvertisementView),
        web.patch("/adv/{adv_id:\d+}", AdvertisementView),
        web.delete("/adv/{adv_id:\d+}", AdvertisementView),
        web.post("/login", LoginView)
    ]
)

web.run_app(app)
