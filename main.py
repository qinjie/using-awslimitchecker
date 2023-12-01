from typing import List,Tuple
import logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

from awslimitchecker.checker import AwsLimitChecker

regions = ['ap-southeast-1', 'ap-northeast-1']

def check_limit_by_region(region: str)-> Tuple[List[str],List[str]]:
    """
    Find the list of services which has reached warning or critical usage limit.
    Arguments:
        region: aws region code
    Returns:
        A tuple contains warning list and critical list, where each item in the list is a comma-delimited value "service,limit_name,usage,limit".
    """
    c = AwsLimitChecker(region=region)

    # Skip CloudTrail because it will cause an error
    c.remove_services(['CloudTrail'])

    warnings = []
    criticals = []
    result = c.check_thresholds()
    for service, svc_limits in result.items():
        for limit_name, limit in svc_limits.items():
            for warn in limit.get_warnings():
                warnings.append(f'{service},{limit_name},{str(warn)},{limit.get_limit()}')

            for crit in limit.get_criticals():
                criticals.append(f'{service},{limit_name},{str(crit)},{limit.get_limit()}')

    return warnings, criticals

for region in regions:
    warnings,criticals = check_limit_by_region(region)
    if warnings:
        print(f'\nWarning: {region}')
        for item in warnings:
            service,limit_name,usage,limit = item.split(',')
            print(f'\t{service}: {limit_name} {usage} <= {limit}')

    if criticals:
        print(f'\nCritical: {region}')
        for item in criticals:
            service,limit_name,usage,limit = item.split(',')
            print(f'\t{service}: {limit_name} {usage} <= {limit}')
