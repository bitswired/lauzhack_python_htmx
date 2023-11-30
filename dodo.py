def task_server_dev():
    return {
        "actions": ["litestar --app lauzhack_pictorial.app:app run --reload -d"],
    }


def task_tailwind_dev():
    return {
        "actions": ["tailwindcss -i input.css -o static_tailwind/output.css --watch"],
    }


def task_dev():
    yield {"name": "server", **task_server_dev()}
    yield {"name": "tailwind", **task_tailwind_dev()}


def task_db_reset():
    return {
        "actions": ["dbmate drop && dbmate up"],
    }


# tailwindcss -i input.css -o output.css --watch
# tailwindcss -i input.css -o output.css --minify
