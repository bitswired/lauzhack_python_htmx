import faker
from litestar import Controller, Router, get
from litestar.response import Template


class LiveDataController(Controller):
    path = "/"

    @get()
    async def index_view(self) -> Template:
        return Template(
            template_name="live-data/index.html",
        )

    @get("/data")
    async def get_live_data(self) -> Template:
        # generate fake stock data
        fake = faker.Faker()
        data = {
            "name": fake.company(),
            "price": fake.pyfloat(left_digits=4, right_digits=2, positive=True),
            "change": fake.pyfloat(left_digits=2, right_digits=2, positive=True),
        }

        return Template(
            template_name="live-data/data-update.html",
            context={
                "data": data,
            },
        )


live_data_router = Router(path="/live-data", route_handlers=[LiveDataController])
