import asyncio
import datetime
from twscrape import API, gather

query_files = ["immigrant", "lgbtq", "misogyny", "xenophobia"]
searches_per_query = 35

start_date = datetime.date(year=2023, month=5, day=18)
end_date = datetime.date(year=2023, month=10, day=27)

one_day = datetime.timedelta(days=1)

def read_queries():
    query_dict = {}
    for file_name in query_files:
        query_dict[file_name] = open("queries\\" + file_name + "_query.txt").readline()
    return query_dict

async def main():
    api = API()
    await api.pool.login_all()

    query_dict = read_queries()

    interval_start = start_date
    
    interval_end = interval_start + one_day

    start_filter = "since:" + str(interval_start) + " "
    end_filter = "until:" + str(interval_end) + " "

    while True:
        if interval_start > end_date:
            break
        else:
            interval_end = interval_start + one_day

        start_filter = " since:" + str(interval_start)
        end_filter = " until:" + str(interval_end)

        for query_name in query_dict.keys():
            tweet_list = await gather(api.search(query_dict[query_name] + start_filter + end_filter, limit=searches_per_query))
            
            file = open("tweet_data\\" + query_name + "\\" + str(interval_start) + ".json", "a")
            file.write("[\n")
            for i in range(len(tweet_list)):
                file.write(tweet_list[i].json())
                if i != len(tweet_list) - 1:
                    file.write(",\n")
            file.write("\n]")
        interval_start = interval_end

asyncio.run(main()) 