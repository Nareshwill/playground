data = {
    "config-ami-check": {
        "loading": False,
        "error": "",
        "info": [
            {
                "region": "ap-northeast-1",
                "ami": "An error occurred (InvalidAMIID.NotFound) when calling the DescribeImages operation: The image id '[ami-0c7fe07fc500c52c4]' does not exist",
                "subnet": {
                    "id": "subnet-08b30123",
                    "AvailabilityZone": "ap-northeast-1d",
                    "VpcId": "vpc-c307e9a5",
                    "State": "available",
                    "region": "ap-northeast-1"
                },
                "securityGroup": {
                    "id": "sg-2d263c63",
                    "Name": "default",
                    "region": "ap-northeast-1"
                }
            },
            {
                "region": "us-east-2",
                "ami": "An error occurred (InvalidAMIID.NotFound) when calling the DescribeImages operation: The image id '[ami-022ff373521efa2a8]' does not exist",
                "subnet": {
                    "id": "subnet-2658874d",
                    "AvailabilityZone": "us-east-2a",
                    "VpcId": "vpc-0861d663",
                    "State": "available",
                    "region": "us-east-2"
                },
                "securityGroup": {
                    "id": "sg-d7ad6fa9",
                    "Name": "default",
                    "region": "us-east-2"
                }
            }
        ]
    },
    "terraform-check": {
        "loading": False,
        "error": "",
        "info": [
            {
                "region": "ap-northeast-1",
                "worker_ami_copy": "An error occurred (InvalidAMIID.NotFound) when calling the DescribeImages operation: The image id '[ami-0756a473c9e1d57fa]' does not exist",
                "s3_bucket": {
                    "tf_config": "cclp-bench-data-dev-01",
                    "app_config": "cclp-bench-data-dev-01"
                },
                "worker_instance_info": {
                    "instance_count": 1,
                    "instance_type": "t2.xlarge"
                },
                "worker_key_pair": {
                    "KeyName": "honda-reprocessing-demo-001",
                    "KeyPairId": "key-055c19a05c79c1460"
                },
                "worker_security_group": "An error occurred (InvalidGroup.NotFound) when calling the DescribeSecurityGroups operation: The security group 'sg-0b3677203b4aaef92' does not exist",
                "worker_subnet": "An error occurred (InvalidSubnetID.NotFound) when calling the DescribeSubnets operation: The subnet ID 'subnet-03cc208f0287e22e9' does not exist"
            },
            {
                "region": "us-east-2",
                "config_path": "File not found"
            }
        ]
    },
    "mongo-connection": {
        "loading": False,
        "error": "",
        "info": {
            "ok": 1
        }
    },
    "rabbitmq-connection": {
        "loading": False,
        "error": "Error occurred while fetching this request!"
    },
    "sqs-queue-length": {
        "loading": False,
        "error": "",
        "info": [
            {
                "region": "ap-northeast-1",
                "ap-northeast-1": {
                    "prod_instance_queue": "0 Messages",
                    "prod_clean_push_play_queue": "0 Messages",
                    "prod_pull_and_terminate_queue": "0 Messages",
                    "prod_aws_available_instances_queue": "0 Messages",
                    "prod_create_instance_failed_queue": "0 Messages",
                    "prod_permanent_failed_queue": "0 Messages",
                    "prod_terminated_instance_queue": "0 Messages",
                    "prod_docker_available_queue": "0 Messages"
                }
            },
            {
                "region": "us-east-2",
                "us-east-2": {
                    "prod_instance_queue": "0 Messages",
                    "prod_clean_push_play_queue": "0 Messages",
                    "prod_pull_and_terminate_queue": "0 Messages",
                    "prod_aws_available_instances_queue": "0 Messages",
                    "prod_create_instance_failed_queue": "0 Messages",
                    "prod_permanent_failed_queue": "0 Messages",
                    "prod_terminated_instance_queue": "0 Messages",
                    "prod_docker_available_queue": "0 Messages"
                }
            }
        ]
    },
    "d62f1f17-71e6-42b7-8df4-3eb613045e21": {
        "loading": False,
        "error": "",
        "info": {
            "scenario_group": {
                "20210915_Group_31_10k_exec__0": "Group not exist",
                "20210915_Group_3_10k_exec__0": "Group not exist",
                "20210915_Group_10_10k_exec__0": "Group not exist",
                "20210915_Group_9_10k_exec__0": "Group not exist",
                "20210915_Group_12_10k_exec__0": "Group not exist",
                "20210915_Group_24_10k_exec__0": "Group not exist",
                "20210915_Group_2_10k_exec__0": "Group not exist",
                "20210915_Group_19_10k_exec__0": "Group not exist",
                "20210915_Group_37_10k_exec__0": "Group not exist",
                "20210915_Group_38_10k_exec__0": "Group not exist",
                "20210915_Group_22_10k_exec__0": "Group not exist",
                "20210915_Group_21_10k_exec__0": "Group not exist",
                "20210915_Group_35_10k_exec__0": "Group not exist",
                "20210915_Group_6_10k_exec__0": "Group not exist",
                "20210915_Group_28_10k_exec__0": "Group not exist",
                "20210915_Group_16_10k_exec__0": "Group not exist",
                "20210915_Group_23_10k_exec__0": "Group not exist",
                "20210915_Group_27_10k_exec__0": "Group not exist",
                "20210915_Group_7_10k_exec__0": "Group not exist",
                "20210915_Group_30_10k_exec__0": "Group not exist",
                "20210915_Group_25_10k_exec__0": "Group not exist",
                "20210915_Group_33_10k_exec__0": "Group not exist",
                "20210915_Group_34_10k_exec__0": "Group not exist",
                "20210915_Group_14_10k_exec__0": "Group not exist",
                "20210915_Group_8_10k_exec__0": "Group not exist",
                "20210915_Group_15_10k_exec__0": "Group not exist",
                "20210915_Group_39_10k_exec__0": "Group not exist",
                "20210915_Group_1_10k_exec__0": "Group not exist",
                "20210915_Group_40_10k_exec__0": "Group not exist",
                "20210915_Group_18_10k_exec__0": "Group not exist",
                "20210915_Group_29_10k_exec__0": "Group not exist",
                "20210915_Group_26_10k_exec__0": "Group not exist",
                "20210915_Group_17_10k_exec__0": "Group not exist",
                "20210915_Group_5_10k_exec__0": "Group not exist",
                "20210915_Group_36_10k_exec__0": "Group not exist",
                "20210915_Group_11_10k_exec__0": "Group not exist",
                "20210915_Group_20_10k_exec__0": "Group not exist",
                "20210915_Group_32_10k_exec__0": "Group not exist",
                "20210915_Group_13_10k_exec__0": "Group not exist",
                "20210915_Group_4_10k_exec__0": "Group not exist"
            }
        }
    }
}


def validate(d):
    for key, value in d.items():
        if isinstance(value, dict):
            validate(value)
        elif isinstance(value, list):
            for doc in value:
                validate(doc)
        else:
            if key == "error" and value != "":
                print({'message': value}, key)
                return {'message': value}
            elif isinstance(value, str) and "error" in value:
                print({'message': value}, key)
                return {"message": value}


if __name__ == "__main__":
    response = validate(data)
    print(response)
