import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

async def main():
    api = API()  # or API("path-to.db") - default is `accounts.db`
    await api.pool.login_all()

    # search (latest tab)
    lgbt_search = "(LGBTQ OR LGBTQ OR LGBT OR homosexual OR gay OR homosexuality OR fags OR faggots OR transexual OR tranny OR trannie OR trannies OR trans OR sodomite) AND (grooming OR groomer OR groomers OR paedophiles OR pedophiles OR paedo OR pedo OR predator OR pervert OR molester OR molest) OR LGBTP."
    i = 0
    async for tweet in api.search(lgbt_search, limit=100):
        i += 1
    print(i)

asyncio.run(main()) 