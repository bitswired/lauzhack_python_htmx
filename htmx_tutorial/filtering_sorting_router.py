import faker
from litestar import Controller, Router, get
from litestar.response import Template

# Random data for filtering and sorting
faker = faker.Faker()
data_filtering_sorting = [
    {
        "name": faker.name(),
        "age": faker.pyint(min_value=18, max_value=100),
        "email": faker.email(),
        "city": faker.city(),
        "country": faker.country(),
        "phone": faker.phone_number(),
    }
    for _ in range(100)
]


class FilteringSortingController(Controller):
    path = "/"

    @get()
    async def index_view(self) -> Template:
        return Template(
            template_name="filtering-sorting/index.html",
            context={
                "clients": data_filtering_sorting,
            },
        )

    @get("/process")
    async def process(
        self,
        sort: str,
        filter: str,
    ) -> Template:
        print(filter, sort)

        if filter:
            data = [
                client
                for client in data_filtering_sorting
                if filter.lower() in client["name"].lower()
            ]
        else:
            data = data_filtering_sorting

        if sort != "none":
            data = sorted(data, key=lambda x: x[sort])

        return Template(
            template_name="filtering-sorting/content.html",
            context={
                "clients": data,
            },
        )


filtering_sorting_router = Router(
    path="/filtering-sorting", route_handlers=[FilteringSortingController]
)
