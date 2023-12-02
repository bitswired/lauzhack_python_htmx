# LauzHack Workshop: Python + HTMX

## How to use

### HTMX Tutorial

1. Clone the repository
2. Install poetry
3. Run `poetry install`
4. Enter the env shell: `poetry shell`
5. Run `doit -n 2 dev_tutorial`

### Fully featured app

1. Clone the repository
2. Install poetry
3. Install Dbmate
4. Run `poetry install`
5. Enter the env shell: `poetry shell`
6. Create a `.env`
7. Add to the `.env`: `DATABASE_URL=sqlite:db/db.sqlite3`
8. Add to the `.env`: `OPENAI_API_KEY=<YOUR_API_KEY>`
9. Run `doit -n 2 db_reset`
10. Run `doit -n 2 db_reset`
