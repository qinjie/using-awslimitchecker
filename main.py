from awslimitchecker.checker import AwsLimitChecker
from typing import List, Tuple
import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


regions = ['ap-southeast-1', 'ap-northeast-1']

# Override default thresholds which are 80 and 99 respectively
WARNING_THRESHOLD = 70
CRITICAL_THRESHOLD = 85

# Set custom thresholds for some limits of some services
service_limit_thresholds = [
    # dict(service_name='VPC', limit_name='NAT Gateways per AZ', warn_percent=None, warn_count=2, crit_percent=None, crit_count=3),
]

# Override default limit values with applied limits: [service_name, limit_name, override_value],
service_limit_overrided = [
    ['EBS', 'General Purpose (SSD gp3) volume storage (GiB)', 50*1024],
    ['CloudFront', 'Cache behaviors per distribution', 25]
]


def get_checker(region: str) -> AwsLimitChecker:
    """
    Return an initialized checker with custom and override values applied.
    """
    c = AwsLimitChecker(region=region,
                        warning_threshold=WARNING_THRESHOLD,
                        critical_threshold=CRITICAL_THRESHOLD)

    # print(c.services)
    # print(c.get_limits(service=['VPC']))

    # Set custom threshold for some services
    for thresholds in service_limit_thresholds:
        c.set_threshold_override(**thresholds)

    # Override default limit values with applied limits
    for override_vals in service_limit_overrided:
        c.set_limit_override(*override_vals)

    # Skip CloudTrail because it will cause an error
    c.remove_services(['CloudTrail'])

    return c


def check_limit_by_region(region: str) -> Tuple[List[str], List[str]]:
    """
    Find the list of services which has reached warning or critical usage limit.
    Arguments:
        region: aws region code
    Returns:
        A tuple contains warning list and critical list, where each item in the list is a comma-delimited value "service,limit_name,usage,limit".
    """
    c = get_checker(region)

    warnings = []
    criticals = []
    result = c.check_thresholds()
    for service, svc_limits in result.items():
        for limit_name, limit in svc_limits.items():
            for warn in limit.get_warnings():
                warnings.append(
                    f'{service},{limit_name},{str(warn)},{limit.get_limit()}')

            for crit in limit.get_criticals():
                criticals.append(
                    f'{service},{limit_name},{str(crit)},{limit.get_limit()}')

    return warnings, criticals


if __name__ == '__main__':
    for region in regions:
        warnings, criticals = check_limit_by_region(region)
        if warnings:
            print(f'\nWarning: {region}')
            for item in warnings:
                if len(item.split(',')) == 4:
                    service, limit_name, usage, limit = item.split(',')
                    print(f'\t{service}: {limit_name} {usage} <= {limit}')

        if criticals:
            print(f'\nCritical: {region}')
            for item in criticals:
                if len(item.split(',')) == 4:
                    service, limit_name, usage, limit = item.split(',')
                    print(f'\t{service}: {limit_name} {usage} <= {limit}')
