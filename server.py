#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: robertking
# @Date:   2017-09-23 01:24:29
# @Last Modified by:   robertking
# @Last Modified time: 2017-09-23 12:03:15


import socketserver
import subprocess
import threading
import time


# Emmm... A little bit nasty here.
tasks = [
    type('task', (object,), {'port': 23, 'filename': 'postfix.pyc'}),
    type('task', (object,), {'port': 233, 'filename': 'draw2.pyc'}),
    type('task', (object,), {'port': 2333, 'filename': 'draw3.pyc'}),
    type('task', (object,), {'port': 23333, 'filename': 'draw45.pyc'}),
]

# Log file, line buffing mode.
logfile = open('logs/remote-tester-{}.log'.format(int(time.time())), 'w', buffering=1)
# Lock for log file, keep the output order clean. (Not sure if print would have a lock itself.)
logfile_lock = threading.Lock()


def do_print(s):
    if logfile_lock.acquire():
        logfile.write(s + '\n')
        print(s)    # print to screen
        logfile_lock.release()


class MyServer(socketserver.ThreadingTCPServer, object):
    allow_reuse_address = True

    def handle_timeout(self):
        do_print('Timed out, Disconnecting...')


def create_handler(task_id, task):

    class MyHandler(socketserver.StreamRequestHandler):
        def handle(self):
            do_print('Task {}: Start connection from {} at {}.'.format(
                task_id, self.client_address, time.ctime()
            ))
            # time.strftime('%Y/%m/%d %H:%S')
            self.request.settimeout(180)
            # Promptline removed to make output exactly the same as the reference program.
            # self.wfile.write('Welcome to Remote Tester powered by robertking!\r\n'
            #                  'Enter your test case below, use ctrl+D (in a new line) to terminate the input.\r\n')

            test_case = self.rfile.read()

            try:
                process = subprocess.Popen('python3 {} 2>&1'.format(task.filename), shell=True,
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                do_print('Task {}: receive test case content on connection from {} at {}:\n{}'.format(
                    task_id, self.client_address, time.ctime(),
                    str(test_case)
                ))
                process.stdin.write(test_case)
                ans, err = process.communicate(timeout=15)
                self.request.sendall(ans)
                # self.wfile.write('GLHF : )')
            except Exception:
                # TODO: Specific different Exception types.
                process.kill()
                self.request.sendall(b'Test program not responding. Exiting...')

            do_print('Task {}: Stop connection from {} at {}.'.format(
                task_id, self.client_address, time.ctime()
            ))

    return MyHandler


def run_server(host, task_id, task):
    s = MyServer((host, task.port), create_handler(task_id, task))
    s.serve_forever()


if __name__ == "__main__":
    host = '0.0.0.0'
    do_print('Remote Grader Server started.')

    thds = []

    for task_id, task in enumerate(tasks):
        thd = threading.Thread(target=run_server, args=(host, task_id, task))
        thd.start()
        thds.append(thd)

    for thd in thds:
        thd.join()
