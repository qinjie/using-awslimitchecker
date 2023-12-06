# Using awslimitchecker

A sample script to use [awslimitchecker](https://github.com/jantman/awslimitchecker) to identify services near their usage limit.

### Note

1. Include CloudTrail service will cause an error during execution. Need to exclude it in the script.

```
c.remove_services(['CloudTrail'])
```

### Sample Output

```
Critical: ap-southeast-1
	EC2: VPC Elastic IP addresses (EIPs) 5 <= 5
	VPC: VPCs 5 <= 5.0
	VPC: Internet gateways 5 <= 5.0
```
