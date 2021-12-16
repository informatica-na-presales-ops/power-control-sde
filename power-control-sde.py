import apscheduler.schedulers.blocking
import boto3
import notch
import os

log = notch.make_log('power_control_sde')


def get_instances():
    # INSTANCE_IDS="i-12345,i-23456"
    instance_ids = os.getenv('INSTANCE_IDS').split(',')
    region = os.getenv('AWS_REGION', 'us-west-2')

    ec2 = boto3.resource('ec2', region_name=region)
    instances = ec2.instances.filter(InstanceIds=instance_ids)
    return instances


def start_instances():
    for instance in get_instances():
        log.info(f'Starting instance {instance.id}')
        instance.start()


def stop_instances():
    for instance in get_instances():
        log.info(f'Stopping instance {instance.id}')
        instance.stop()


if __name__ == '__main__':
    scheduler = apscheduler.schedulers.blocking.BlockingScheduler()
    scheduler.add_job(start_instances, 'cron', day_of_week='0-4', hour=4, minute=0)
    scheduler.add_job(stop_instances, 'cron', hour=19, minute=0)
    scheduler.start()
