#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: wenbin
@filename: test
@created date: 2017/8/4
@last modified: 2017/8/4
"""
from quartz.universe.screener import StockScreener
import requests
from itertools import product
import pandas as pd
import threading
import queue

df = pd.DataFrame(columns=('factor', 'universe_type', 'report_types'))


def get_cookies(login_url, user_name, password):
    try:
        res = requests.post(login_url,
                            {'username': user_name, 'password': password})
        token = res.json().get('content', {}).get('token', {}).get('tokenString', '')
        #logger.debug(res.content)
    except ValueError:
        raise Exception(u'Response of tokenurl is not json. Please check the properties')
    except Exception:
        try:
            #logger.error(u'response content: {}'.format(res.content.decode('utf-8')))
            pass
        except NameError:
            pass
        #logger.error(traceback.format_exc())
        raise

    if res.status_code != 200:
        raise Exception(u'Username and password is incorrect')
    return {'cloud-sso-token': token}

#auth_url = "https://gw.wmcloud-stg.com/usermaster/authenticate/v1.json"
auth_url = "https://gw.wmcloud.com/usermaster/authenticate/v1.json"
factors = StockScreener.available_factors()
universe_types = ["HSSLL","ZZWLL"]

report_types =["long","year","week","day"]

dicard_items = [i for i in product(factors,universe_types,report_types)]


#cookies = get_cookies(auth_url,"wb.feng@datayes.com","datayes@123")
cookies = get_cookies(auth_url,"wenbin.feng@datayes.com","xxxxx")
headers = {"Content-Type": "application/json"}


def get_factor_attr(args):
    #url = "https://gw.wmcloud-stg.com/mercury_trade/factor/uqer/{factor}/position/20170731?universe_type={universe_type}&report_type={report_type}".format(
    url = "https://gw.wmcloud.com/mercury_trade/factor/uqer/{factor}/position/20170731?universe_type={universe_type}&report_type={report_type}".format(
          factor=args[0], universe_type=args[1], report_type=args[2]
    )
    flag_status = True
    res = requests.get(url, cookies=cookies)
    if res.status_code == 200:
        try:
            data = res.json()["attr_perf"]
            # print args[0],data
            row = None
        except KeyError:
            row = pd.DataFrame([{"factor":args[0],"universe_type":args[1],"report_types":args[2]},])
            flag_status = False
        finally:
            return flag_status, row


def create_threads(jobs, func, results, concurrency):
    for _ in range(concurrency):
        thread = threading.Thread(target=worker, args=(func, jobs, results))
        thread.daemon = True
        thread.start()


def worker(func, jobs, results):
    while True:
        try:
            test_args = jobs.get()
            ok, result_row = func(test_args)
            if not ok:
                # df.append(result_row, ignore_index=True)
                print "{factor_args} is not available".format(factor_args=test_args)
                results.put(result_row)
            elif result_row is None:
                pass
        finally:
            jobs.task_done()


def add_jobs(test_args, jobs):
    for todo, test_arg in enumerate(test_args, start=1):
        jobs.put(test_arg)
    return todo


def process(todo, jobs, results, concurrency):
    canceled = False
    try:
        jobs.join() # Wait for all the work to be done
    except KeyboardInterrupt: # May not work on Windows
        print "canceling..."
        canceled = True
    if canceled:
        done = results.qsize()
    else:
        done, filename = output(results)
    current_process = "read {}/{} feeds using {} threads{}".format(done, todo,
                                                 concurrency, " [canceled]" if canceled else "")
    print current_process
    if not canceled:
        df.to_csv("na_factor.csv")


def output(results):
    done = 0
    while not results.empty():
        result = results.get_nowait()
        done += 1
        df.append(result, ignore_index=True)
    return done, df


def main():
    print "starting..."
    concurrency = 16
    jobs = queue.Queue()
    results = queue.Queue()
    create_threads(jobs, get_factor_attr, results, concurrency)
    todo = add_jobs(dicard_items, jobs)
    process(todo, jobs, results, concurrency)

if __name__ == "__main__":
    import time
    start = time.time()
    main()
    end = time.time()
    print "total time: ",(end-start)/60, "min"
