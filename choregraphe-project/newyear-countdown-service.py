import datetime
import functools
import qi

logcat = 'NewYearCountdown'

# The moments before announcing the next year
announcement_times_data = [{'days':31, 'hours':4}, {'days':20, 'hours':4}, {'days':10, 'hours':4}, {'days':5, 'hours':4}, {'days':3, 'hours':4}, {'days':2, 'hours':4}, {'days':1, 'hours':4}, {'hours':12}, {'hours':8}, {'hours':4}, {'hours':2}, {'hours':1}, {'minutes':30}, {'minutes':15}, {'minutes':5}]

previous_announcement_time_data = {'days':3}

def limited_min(min_limit, current_min, next):
    if current_min < min_limit:
        return min_limit.max
    if next < min_limit:
        return current_min
    return min(next, current_min)

def limited_max(max_limit, current_max, next):
    if current_max > max_limit:
        return max_limit.min
    if next > max_limit:
        return current_max
    return max(next, current_max)

def time_to_new_year():
    '''Computes the time before next year'''
    now = datetime.datetime.now()
    newYear = datetime.datetime(year=now.year + 1, month=1, day=1)
    return newYear - now

def start_final_countdown(session):
    qi.info(logcat, 'Final countdown!')
    life = session.service('ALAutonomousLife')
    life.switchFocus('new-year-countdown/Final Countdown')

def announce_and_schedule(session, previous_announcement_time, announcement_times):
    '''Announces the time left before new year and updates the previous announcement time, before scheduling the next announcement time'''
    time_limit = time_to_new_year()

    # Announce if needed
    qi.info(logcat, 'Last announcement made was %s before new year' % previous_announcement_time)
    latest_announcement_time = reduce(functools.partial(limited_min, time_limit), announcement_times)
    if latest_announcement_time < previous_announcement_time:
        qi.info(logcat, 'Announcement missed %s before new year, go for it!' % latest_announcement_time)
        memory = session.service('ALMemory')
        memory.setData('NewYearCountDown', '%s;%s;%s' % (previous_announcement_time.days, previous_announcement_time.hours, previous_announcement_time.minutes))
        life = session.service('ALAutonomousLife')
        life.switchFocus('new-year-countdown/Announce Time Left')
        previous_announcement_time = latest_announcement_time

    # Schedule next announce
    next_announcement_time = reduce(functools.partial(limited_max, time_limit), announcement_times)
    time_to_next_announcement = time_limit - next_announcement_time

    qi.info(logcat, 'Next announcement scheduled in %s' % time_to_next_announcement)
    qi.async(announce_and_schedule, session, previous_announcement_time, announcement_times, delay=int(time_to_next_announcement.total_seconds()+1)*1000000)

if __name__ == '__main__':
    app = qi.Application()
    app.start() # connects the session

    previous_announcement_time = datetime.timedelta(**previous_announcement_time_data)

    announcement_times = list()
    for time_data in announcement_times_data:
        announcement_times.append(datetime.timedelta(**time_data))

    announce_and_schedule(app.session, previous_announcement_time, announcement_times)

    time_to_final_countdown = time_to_new_year() - datetime.timedelta(seconds=60)
    qi.info(logcat, 'Final countdown scheduled in %s' % time_to_final_countdown)
    qi.async(start_final_countdown, app.session, delay=int(time_to_final_countdown.total_seconds()*1000000))

    app.run()
