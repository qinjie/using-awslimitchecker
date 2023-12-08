# Using awslimitchecker

A sample script to use [awslimitchecker](https://github.com/jantman/awslimitchecker) to identify services near their usage limit.

### Note

This library is slightly outdated. It should be

1. Including CloudTrail service will cause an error during execution. Need to exclude it in the script.

```
c.remove_services(['CloudTrail'])
```

2. The actual CloudFront quotas are not available in the Service Quota SDK. Thus we need to submit an AWS Support case to find out the actual applied quota.

```
c.set_limit_override('CloudFront', '<QUOTA_NAME>', <QUOTA_VALUE>)
```

3. The limit `EBS: General Purpose (SSD gp3) volume storage (GiB)` should be `EBS: Storage for General Purpose SSD (gp3) volumes, in TiB`. Find the applied quota from https://ap-southeast-1.console.aws.amazon.com/servicequotas/home/services/ebs/quotas/L-7A658B76 (Update region value accordingly), and add following statements.

```
c.set_limit_override('EBS', 'General Purpose (SSD gp3) volume storage (GiB)', <QUOTA_VALUE>)
```

### Sample Output

```
Critical: ap-southeast-1
	EC2: VPC Elastic IP addresses (EIPs) 5 <= 5
	VPC: VPCs 5 <= 5.0
	VPC: Internet gateways 5 <= 5.0
```
