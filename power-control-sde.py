import apscheduler
import boto3
import os


def get_instances():
    # INSTANCE_IDS="i-12345,i-23456"
    instance_ids = os.getenv('INSTANCE_IDS').split(',')

    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(InstanceIds=instance_ids)
    return instances


def start_instances():
    for instance in get_instances():
        instance.start()


def stop_instances():
    for instance in get_instances():
        instance.stop()


if __name__ == '__main__':
    scheduler = apscheduler.schedulers.blocking.BlockingScheduler()
    scheduler.add_job(start_instances, 'cron', day_of_week='0-4', hour=7, minute=0)
    scheduler.add_job(stop_instances, 'cron', hour=21, minute=0)
    scheduler.start()
