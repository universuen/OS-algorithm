from decimal import Decimal as D

class Job():
    def __init__(self, submit:float, duration:float):
        self.submit = D(str(submit))  # 提交时间
        self.duration = D(str(duration))  # 运行时间
        self.start = None  # 开始时间
        self.finish = None  # 完成时间
        self.tat = None  # Turnaround time 周转时间
        self.tat_w = None  # Weighted turnaround time 带权周转时间
        self.remain = D(str(duration))  # 剩余时间
        self.slice = None  # 时间片大小，仅用于RR
        self.rr = None  # Response ratio 响应比，仅用于HRRN

# 先来先服务
def FCFS(jobs:list):
    # 未到达作业队列
    remain_jobs = jobs.copy()
    # 按照提交时间排序
    remain_jobs.sort(key=lambda x: x.submit)
    time = D(str(0))
    # 依次处理作业
    for i in remain_jobs:
        if i.submit > time:
            time = i.submit
        i.start = time
        time += i.duration
        i.finish = time
        i.tat = i.finish - i.submit
        i.tat_w = i.tat / i.duration
        i.remain -= i.duration

# 短作业优先
def SFJ(jobs:list):
    # 未到达作业队列
    remain_jobs = jobs.copy()
    # 按照提交时间排序
    remain_jobs.sort(key=lambda x: x.submit)
    # 已到达但是在等待的作业序列
    waiting_jobs = []
    time = D(str(0))
    # 循环处理，直到没有剩余作业
    while len(remain_jobs) > 0 or len(waiting_jobs) > 0:
        # 如果就绪队列为空则快进
        if len(waiting_jobs) == 0:
            remain_jobs.sort(key=lambda x:x.submit)
            time = remain_jobs[0].submit
        else:
            # 泵出就绪队列中剩余时间最少的作业
            waiting_jobs.sort(key=lambda x: x.duration)
            job = waiting_jobs.pop(0)
            # 处理
            job.start = time
            time += job.duration
            job.finish = time
            job.tat = job.finish - job.submit
            job.tat_w = job.tat / job.duration
            job.remain -= job.duration
        # 查看是否有新的作业就绪
        for i in remain_jobs:
            if i.submit <= time:
                waiting_jobs.append(i)
        for i in waiting_jobs:
            if i in remain_jobs:
                remain_jobs.remove(i)

# 最短剩余时间优先
def SRTF(jobs:list):
    # 未到达作业队列
    remain_jobs = jobs.copy()
    # 按照提交时间排序
    remain_jobs.sort(key=lambda x: x.submit)
    # 已到达但是在等待的作业序列
    waiting_jobs = []
    time = D(str(0))
    processing = False
    # 循环处理，直到没有剩余作业
    while len(remain_jobs) > 0 or len(waiting_jobs) > 0 or processing == True:
        if not processing:
            if len(waiting_jobs) != 0:
                waiting_jobs.sort(key=lambda x:x.remain)
                job = waiting_jobs.pop(0)
                if job.start == None:
                    job.start = time
            else:
                job = remain_jobs.pop(0)
                time = job.submit
                job.start = time
            processing = True
        else:
            # 还有作业未到达
            if len(remain_jobs) != 0:
                next_job = remain_jobs.pop(0)
                # 下一个作业到来之前能完成当前作业
                if time + job.remain <= next_job.submit:
                    time += job.remain
                    job.remain -= job.remain
                    job.finish = time
                    job.tat = job.finish - job.submit
                    job.tat_w = job.tat / job.duration
                    processing = False
                # 下一个作业到来之前不能完成当前作业
                else:
                    job.remain -= next_job.submit - time
                    time = next_job.submit
                    # 抢占
                    if next_job.remain < job.remain:
                        waiting_jobs.append(job)
                        job = next_job
                        job.start = time
                    # 未抢占
                    else:
                        waiting_jobs.append(next_job)
            # 所有作业已到达
            else:
                time += job.remain
                job.remain -= job.remain
                job.finish = time
                job.tat = job.finish - job.submit
                job.tat_w = job.tat / job.duration
                processing = False

# 时间片轮转
def RR(jobs:list, slice_size = 1):
    # 设置时间片大小
    slice_size = D(str(slice_size))
    # 未到达作业队列
    remain_jobs = jobs.copy()
    # 按照提交时间排序
    remain_jobs.sort(key=lambda x: x.submit)
    for i in  remain_jobs:
        i.slice = slice_size
    time = D(str(0))
    waiting_jobs = []
    processing = False
    while len(remain_jobs) > 0 or len(waiting_jobs) > 0 or processing == True:
        if not processing:
            if len(waiting_jobs) > 0:
                job = waiting_jobs.pop(0)
                if job.start == None:
                    job.start = time
            else:
                job = remain_jobs.pop(0)
                job.start = time
            processing = True
        else:
            if len(remain_jobs) > 0:
                next_job = remain_jobs[0]
                if time == next_job.submit:
                    waiting_jobs.append(next_job)
                    remain_jobs.pop(0)
            if job.slice > 0:
                time += 1
                job.slice -= 1
                job.remain -= 1
                if job.remain == 0:
                    job.finish = time
                    job.tat = job.finish - job.submit
                    job.tat_w = job.tat / job.duration
                    processing = False
            else:
                job.slice = slice_size
                waiting_jobs.append(job)
                processing = False

# 高响应比优先
def HRRN(jobs: list):
    # 未到达作业队列
    remain_jobs = jobs.copy()
    # 按照提交时间排序
    remain_jobs.sort(key=lambda x: x.submit)
    # 已到达但是在等待的作业序列
    waiting_jobs = []
    time = D(str(0))
    processing = False
    # 循环处理，直到没有剩余作业
    while len(remain_jobs) > 0 or len(waiting_jobs) > 0 or processing == True:
        if not processing:
            if len(waiting_jobs) > 0:
                # 更新响应比
                for i in waiting_jobs:
                    i.rr = D(str(1)) + ((time - i.submit) / i.duration)
                # 泵出响应比最高的作业
                waiting_jobs.sort(key=lambda x:x.rr, reverse=True)
                job = waiting_jobs.pop(0)
                job.start = time
            else:
                job = remain_jobs.pop(0)
                time = job.submit
                job.start = time
            processing = True
        else:
            time += job.duration
            job.finish = time
            job.tat = job.finish - job.submit
            job.tat_w = job.tat / job.duration
            job.remain -= job.duration
            processing = False
            # 查看是否有新的作业到达
            for i in remain_jobs:
                if i.submit <= time:
                    waiting_jobs.append(i)
            for i in waiting_jobs:
                if i in remain_jobs:
                    remain_jobs.remove(i)

def display(jobs:list):
    sum_tat = D(str(0))
    sum_tat_w = D(str(0))
    for i in range(len(jobs)):
        print('--------------------------')
        print('作业序号:', i+1)
        print('提交时间:', jobs[i].submit)
        print('运行时间:', jobs[i].duration)
        print('开始时间:', jobs[i].start)
        print('完成时间:', jobs[i].finish)
        print('周转时间:', jobs[i].tat)
        print('带权周转时间:', jobs[i].tat_w)
        sum_tat += jobs[i].tat
        sum_tat_w += jobs[i].tat_w
    print('--------------------------')
    print('平均周转时间:', sum_tat/D(len(jobs)))
    print('平均带权周转时间:', sum_tat_w/D(len(jobs)))

if __name__ == '__main__':
    # job_num = int(input('请输入作业个数:'))
    # jobs = []
    # for i in range(job_num):
    #     print('----------------------------')
    #     submit = float(input('请输入第' + str(i+1) + '个作业的提交时间:'))
    #     duration = float(input('请输入第' + str(i+1) + '个作业的运行时间:'))
    #     job = Job(submit, duration)
    #     jobs.append(job)
    # print('----------------------------')
    # print('1.先来先服务FCFS')
    # print('2.短作业优先SFJ')
    # print('3.最短剩余时间优先')
    # print('4.时间片轮转')
    # choice = input('请选择调度算法:')
    # if choice == '1':
    #     FCFS(jobs)
    # elif choice == '2':
    #     SFJ(jobs)
    # elif choice == '3':
    #     SRTF(jobs)
    # elif choice == '4':
    #     slice = int(input('请输入时间片大小:'))
    #     RR(jobs, slice)
    # display(jobs)
    jobs = [
        Job(0, 3),
        Job(2, 6),
        Job(4, 4),
        Job(6, 5),
        Job(8, 2)
    ]
    RR(jobs)
    display(jobs)
