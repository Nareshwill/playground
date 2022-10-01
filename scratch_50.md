## How to Set up & Schedule Execution in AWS Cloud using SIL Framework.

* Prerequisite
  * AWS Account with appropriate privileges
  * Ubuntu 18.04 LTS
  * Database instance up & running (Can be/Can't be replicated.)


### Setting up the application.
#### Step 1: Creation of an EC2 Instance/ Use an existing EC2 Instance. (If you are creating an EC2 instance make sure you are appropriate enabling auto assign public IP, subnet, VPC & security groups).
#### Step 2: Copy the repository to spawned EC2 instance.
#### Step 3: Create a virtual environment & Install all the required packages from requirements.txt
#### Step 4: Configuration changes.
```json
    {
      "APPLICATION_DEFAULT_LANDING_PAGE":"",
      "DATABASE_URI": "mysql+pymysql://<username>:<password>@<database-ip>/test_manager",
      "SCENARIO_CATALOGUE_DB_URI": "mysql+pymysql://<username>:<password>@<database-ip>/tm_scenario_catalogue",
      "SCENE_GEN_DB_URI": "mysql+pymysql://<username>:<password>@<database-ip>/tm_scene_gen",
      "CLOSED_LOOP_DB_URI" : "mysql+pymysql://<username>:<password>@<database-ip>/tm_close_loop",
      "TJA_V2_AUTOMATE_KPI_DB_URI": "mysql+pymysql://<username>:<password>@<database-ip>/tm_automate_kpi_tja_v2",
      "CUSTOM_MAP_BENCH_PATH" : "/home/rajivt/code/scenario_simulation/source/replay_agent_v002/CarlaSim/CarlaUE4/Content/Custom_Maps/Maps",
      "AD_CLIENT_BENCH_PATH": "/home/rajivt/code/scenario_simulation/source/replay_agent_v002/ad_client_server",
      "REPORT_GEN_DB_URI": "mysql+pymysql://<username>:<password>@<database-ip>/tm_close_loop_execution_report",
      "SCENARIO_CATALOGUE_MONGO_DB_NAME": "simulib",
      "CLOSE_LOOP_MONGO_DB": "close_loop_validation - MongoDB Database Name",
      "DB_SERVER": "<database-ip>",
      "DB_NAME": "test_manager",
      "DB_NAME_TJA": "tm_close_loop",
      "DB_AUTOMATE_KPI_TJA_V2": "tm_automate_kpi_tja_v2",
      "DB_SCENARIO_CATALOGUE": "tm_scenario_catalogue",
      "DB_SCENE_GEN": "tm_scene_gen",
      "DB_REPORT_GEN": "tm_close_loop_execution_report",
      "DB_USER": "database - <username>",
      "DB_PWD": "database - <password>",
      "MONGO_DATABASE": "scenario_catalogue",
      "LKA_DATABASE":"LKAScenarioExtractor",
      "MONGO_SERVER": "<database-ip>",
      "MONGO_PORT": 27017,
      "MONGO_USERNAME" : "database - <username>",
      "MONGO_PWD" : "database - <password>",
      "KPI_DASHBOARD_MONGO_ENABLED" : true,
      "VERSION": "1.0.5.11811",
      "SECRET_KEY": "9583ab3c7b46619bf457747609f3ec95",
      "DB_URI": "mysql+pymysql://<username>:<password>@<database-ip>/test_manager",
      "LOG_FILE": "app.log",
      "BENCH_PING_TIMEOUT" : 5,
      "REST_CLUSTER_COORDINATOR": ["localhost", "localhost", "localhost", "localhost", "localhost"],
      "PORT" : "3000",
      "SCHEME":"http",
      "DATASET":"/home/rajivt/code/scenario_simulation/source/sample/data/ground_truth_sample_sweep/Mini_dataset",
      "MODE":"developer",
      "MAX_EXPECTED_GROUP_NUMBER":"500",
      "AWS_ENABLED": true <enable it to use aws services>,
      "PARTIAL_PULL" : "true",
      "AWS_S3_ENABLED": true <enable it to use s3 service>,
      "DOCKER_ENABLED": true <enable it to execute your scenario inside a container>,
      "DOCKER_COUNT": 4 <mention the number of containers used>,
      "S3_BUCKET_NAME": "cclp-bench-data-dev-01 <mention the bucker to access input data and store output data>",
      "REGION_NAME": "ap-south-1 <mention the region from where you want access the aws service>",
      "CELERY_CONFIG": {
        "activate": true,
        "root": "/home/rajivt/code/scenario_simulation/source/server_app_v001/tmp <mention the folder where celery need to store the meta data>",
        "broker_url": "filesystem://",
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": [
          "json"
        ],
        "persist_results": true,
        "CAD_CONFIG":{
          "create_aws_instance_enabled":true,
          "create_aws_instance_delay":5,
          "clean_push_play_enabled":true,
          "clean_push_play_delay":5,
          "pull_and_terminate_instance_enabled":true,
          "pull_and_terminate_delay":5,
          "retry_failed_kpi_extraction_cases_enabled": false,
          "retry_failed_kpi_extraction_cases_delay": 30,
          "reconcilation_system_workflow_enabled" : true,
          "reconcilation_system_workflow_delay" : 30,
          "public_or_private_ip_connector":"private",
          "celery_periodic_task_frequency":20,
          "IP_developers_machines":["127.0.0.1","localhost"],
          "max_aws_permitted_instances" : 200,
          "max_retry_counter":421000,
          "visibility_timeout_create_instance" : 30,
          "visibility_timeout_push_scenario" : 30,
          "visibility_timeout_pull_scenario" : 30,
          "reconcilation_retry_count": 8400
        },
        "SCENARIO_VARIATION_CONFIG":{
            "OpenSCENARIO_xsd_path":"/home/rajivt/code/scenario_simulation/source/server_app_v001/scenario_variation_generator/utility/OpenSCENARIO.xsd",
            "scenario_variation_generator_directory": "/home/rajivt/code/scenario_simulation/source/sample/data/Scenario_Variation_Inputs"
        }
      },
      "CUSTOM_MAP_AND_AD_CLIENT_UPLOAD":"/home/rajivt/code/scenario_simulation/source/sample/data/Custom_Map_AD_Client",
      "SCENARIO_FILE_UPLOAD": {
        "MAX_CONTENT_LENGTH": 61440000,
        "UPLOAD_EXTENSIONS" : [".docx", ".zip", ".xosc", ".xml", ".txt"],
        "BUCKET_CONFIGURATION": {
          "SCENARIO_VARIATION_FILES":"data/temp/scenario_variation_files",
          "SCENARIO_FILES": "data/temp/scenario_files",
          "SCENARIO_REPRESENTATION": "data/temp/scenario_representation"
        },
        "LOCAL_CONFIGURATION": {
          "SCENARIO_FILES": "/home/rajivt/code/scenario_simulation/source/sample/data/carla_scenarios",
          "SCENARIO_REPRESENTATION": "/home/rajivt/code/scenario_simulation/source/server_app_v001/Resource/default_img"
        }
      },
      "KPI": {
        "TJA_KPI_LIST": ["lane_management_kpi", "longitudinal_motion_kpi", "safe_driving_kpi", "ego_velocity"],
        "LEVEL0_KPI_LIST": ["l0_collision_check_kpi", "l0_lateral_safe_distance_kpi", "l0_longitudinal_safe_distance_kpi", "l0_offroad_check_kpi", "l0_lane_marking_check_kpi", "l0_indicator_checking_kpi", "l0_speed_limit_check_kpi", "l0_false_indicator_check_kpi"],
        "LEVEL1_KPI_LIST": ["l1_lateral_acceleration_kpi", "l1_lateral_jerk_kpi", "l1_longitudinal_deceleration_kpi", "l1_longitudinal_acceleration_kpi", "l1_longitudinal_jerk_kpi", "l1_longitudinal_velocity_drop_kpi"],
        "RSS_KPI_LIST": ["rss_longitudinal_safe_check_kpi", "rss_lateral_left_safe_check_kpi", "rss_lateral_right_safe_check_kpi"]
      },
      "GROUND_TRUTH": {
        "GROUND_TRUTH_KPI": "ground_truth_kpi.csv",
        "LEVEL0_LEVEL1_KPI": "level0_level1_kpi.csv",
        "RSS_KPI": "rss_kpi.csv"
      },
      "VALIDATION_CONFIG":{
        "VALIDATION_CLASS":["All"],
        "VALIDATION_TYPE":"specific_gt",
        "CCLP_KPI": {}
      },
      "K_DATA_ANALYZER": {},
      "SCENARIO_EDITOR": {},
      "SCENE_EXTRACT": {},
      "BENCH_DATA": {
      "carlaBenchData": [
        {
          "name": "Carla_Bench_1",
          "address": "localhost",
          "bench_id" : 11,
          "http_port": "8002",
          "ssh_port" : "22",
          "bench_user": "kpit",
          "bench_password": "password",
          "bench_type" : "Carla",
          "server_location_of_bench": "/home/rajivt/code/scenario_simulation/source/sample/data/server/bench-data/carla/bench1",
          "bench_dump_location": "/home/rajivt/code/scenario_simulation/source/sample/data/bench-data/carla/bench1",
          "bench_output_location": "/home/rajivt/code/scenario_simulation/source/sample/data/bench-output/carla/bench1",
          "poll_data_url" : "http://localhost:5000/poll_bench_data",
          "validation_url" : "http://localhost:5000/validation",
          "summary_url" : "http://localhost:5000/summary_report",
          "TEMP_LOCATION" : "/home/rajivt/code/scenario_simulation/source/sample/data/tmp"
        },
        {
          "name": "Carla_Bench2",
          "address": "localhost",
          "bench_id" : 21,
          "http_port": "8002",
          "ssh_port" : "22",
          "bench_user": "rajivt",
          "bench_password": "password",
          "bench_type" : "Carla",
          "server_location_of_bench": "/home/rajivt/code/scenario_simulation/source/sample/data/server/bench-data/carla/bench2",
          "bench_dump_location": "/home/rajivt/code/scenario_simulation/source/sample/data/bench-data/carla/bench2",
          "bench_output_location": "/home/rajivt/code/scenario_simulation/source/sample/data/bench-output/carla/bench2",
          "poll_data_url" : "http://localhost:5000/poll_bench_data",
          "validation_url" : "http://localhost:5000/validation",
          "summary_url" : "http://localhost:5000/summary_report",
          "TEMP_LOCATION" : "/home/rajivt/code/scenario_simulation/source/sample/data/tmp"
        },
        {
          "name": "Carla_Bench3",
          "address": "localhost",
          "bench_id" : 31,
          "http_port": "8002",
          "ssh_port" : "22",
          "bench_user": "rajivt",
          "bench_password": "password",
          "bench_type" : "Carla",
          "server_location_of_bench": "/home/rajivt/code/scenario_simulation/source/sample/data/server-output/bench-data/carla/bench3",
          "bench_dump_location": "/home/rajivt/code/scenario_simulation/source/sample/data/bench-data/carla/bench3",
          "bench_output_location": "/home/rajivt/code/scenario_simulation/source/sample/data/bench-output/carla/bench3",
          "poll_data_url" : "http://localhost:5000/poll_bench_data",
          "validation_url" : "http://localhost:5000/validation",
          "summary_url" : "http://localhost:5000/summary_report",
          "TEMP_LOCATION" : "/home/rajivt/code/scenario_simulation/source/sample/data/tmp"
        }
      ]
      },
      "CLOSE_LOOP_WORKFLOW_QUEUES": {
        "production": [
          "prod_instance_queue",
          "prod_clean_push_play_queue",
          "prod_pull_and_terminate_queue",
          "prod_aws_available_instances_queue",
          "prod_create_instance_failed_queue",
          "prod_permanent_failed_queue",
          "prod_terminated_instance_queue",
          "prod_docker_available_queue"
        ],
        "development": [
          "aws_dev_instance_queue",
          "aws_dev_clean_push_play_queue",
          "aws_dev_pull_and_terminate_queue",
          "aws_dev_aws_available_instances_queue",
          "aws_dev_ip_queue",
          "aws_dev_create_instance_failed_queue",
          "aws_dev_permanent_failed_queue",
          "aws_dev_terminated_instance_queue",
          "aws_docker_available_queue"
        ]
      },
      "SCP_SOCKET_TIMEOUT": 1800,
      "CLOSE_LOOP_SCN_GROUP_INSTANCE_DETAILS": {
        "generate_kpi": "False",
        "generate_scenario_video": "False",
        "signal_alarm": "45",
        "delay_parameter_1": "1.5",
        "delay_parameter_2": "50",
        "mode": "production",
        "no_rendering_mode": "True",
        "carla_quality_level": "-quality-level=Low",
        "max_retrying_count": "3",
        "sampling_frame_rate": "100",
        "instance_id": "i-635adc0b-f6b5-4a49-b390-3aa109809518",
        "ip_address": "127.0.1.1",
        "state": "running",
        "attempt_count": 0,
        "max_force_termination_time_of_scenario": "2000",
        "generate_rss_kpi": "True",
        "bench_flag": "True",
        "generate_level0_level1_kpi": "True",
        "scenario_visualizer_flag": "False",
        "AD_Model_Type": "Honda_Model",
        "custom_map_uuid": "null",
        "ad_client_uuid": "null"
      },
      "DOCKERS_INFO": [
        {
          "docker_container_name": "docker_9001",
          "http_port": "9001",
          "ssh_port": "2222",
          "carla_rpc_port": 2000,
          "traffic_manager_port": 8000,
          "bench_user": "rajivt"
        },
        {
          "docker_container_name": "docker_9002",
          "http_port": "9002",
          "ssh_port": "2223",
          "carla_rpc_port": 3000,
          "traffic_manager_port": 8050,
          "bench_user": "rajivt"
        },
        {
          "docker_container_name": "docker_9003",
          "http_port": "9003",
          "ssh_port": "2224",
          "carla_rpc_port": 4000,
          "traffic_manager_port": 8100,
          "bench_user": "rajivt"
        },
        {
          "docker_container_name": "docker_9004",
          "http_port": "9004",
          "ssh_port": "2225",
          "carla_rpc_port": 5000,
          "traffic_manager_port": 8150,
          "bench_user": "rajivt"
        }
      ],
      "AZURE": {
        "activate": false,
        "enabled": false,
        "GROUP_NAME": "samplegroup",
        "network_security_group_id": "/subscriptions/077d0fee-fb7c-4172-bf23-ffbf17c6ab29/resourceGroups/deploy-backup/providers/Microsoft.Network/networkSecurityGroups/testNSG",
        "AZURE_BLOB_NAME": "cclp-bench-data-dev-01",
        "periodic_task_frequency": 20,
        "subscription_id": "077d0fee-fb7c-4172-bf23-ffbf17c6ab29",
        "tenant_id": "3539451e-b46e-4a26-a242-ff61502855c7",
        "client_id": "e58b86f8-ff72-4013-b82b-0e14903256ad",
        "client_secret": "dzQ3J2VeMMEzOQD0klpsh0sb8AZFJU_eHo",
        "vnet_address_prefix": "['10.0.0.0/16']",
        "subnet_address_prefix": "10.0.0.0/22",
        "storage_connection_string": "DefaultEndpointsProtocol=https;AccountName=kpitstorage2;AccountKey=fqsaQrfxBTaoRU/AoYIvpuBrAyCe3e1lL9p52eYrwmWwYoa/Hbi3Pjahnvk+gDsrsA6/Xr1V5LOqVhWqVKwvrg==;EndpointSuffix=core.windows.net",
        "queue": {
          "production": [
            "instance-queue",
            "clean-push-play-queue",
            "pull-and-terminate-queue",
            "azure-available-instances-queue",
            "create-instance-failed-queue",
            "permanent-failed-queue",
            "terminated-instance-queue"
          ],
          "development": [
            "dev-instance-queue",
            "dev-clean-push-play-queue",
            "dev-pull-and-terminate-queue",
            "dev-aws-available-instances-queue",
            "dev-ip-queue",
            "dev-create-instance-failed-queue",
            "dev-permanent-failed-queue",
            "dev-terminated-instance-queue"
          ]
        }
      },
      "DYNAMIC_SCHEDULING" : {
        "enabled" : true <enable it to use dynamic scheduler>,
        "tf_directory" : "/home/kpit/code/scenario_simulation/source/server_app_v001/terraform_configuration" ,
        "infra" : { 
          "<region>": {
            "bench_ami": "<mention the bench-ami from the region "region">",
            "subnet_id": "<mention the subnet-id from the region "region">",
            "security_group_id" : "<mention the security group id from the region "region">",
            "initiation_count" : 1,
            "worker_count" : 1, <mention the number of instances to spawned in the region "region">
          },
          "us-east-1" : {
            "bench_ami" : "ami-0c7fe07fc500c52c4", <mention the bench-ami from the region "us-east-1">
            "subnet_id" : "subnet-08b30123", <mention the subnet-id from the region "us-east-1">
            "security_group_id" : "sg-2d263c63", <mention the security group id from the region "us-east-1">
            "initiation_count" : 1,
            "worker_count" : 1, <mention the number of instances to spawned in the region "us-east-1">
            "var_file" : "/home/kpit/code/scenario_simulation/source/server_app_v001/terraform_configuration/var_files/virginia.tfvars.json"
         },
          "us-west-2" : {
            "bench_ami" : "ami-022ff373521efa2a8", <mention the bench-ami from the region "us-west-2">
            "subnet_id" : "subnet-2658874d", <mention the subnet-id from the region "us-west-2">
            "security_group_id" : "sg-d7ad6fa9", <mention the security group id from the region "us-west-2">
            "initiation_count" : 1,
            "worker_count" : 1, 
            "var_file" : "/home/kpit/code/scenario_simulation/source/server_app_v001/dynamic_scheduling/terraform_configuration/var_files/oregon.tfvars.json"
          }
        }
      },
      "APM_STREAMS": {
        "host": "<rabbitmq-ip>",
        "username": "<username>",
        "password": "<password>"
      }
```

#### Step 5: Install & Build React production build for frontend
* Navigate to the application root directory `server_app_v001`.
```shell
    cd code/source/server_app_v001
    npm i # to install all the application dependencies.
    npm run build # to create a production build.
```
* Note: While executing `npm run build` You might encounter the following error.
```shell
    FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory
```
* Please execution the following & rerun the `npm run build` again.
```shell
    export NODE_OPTIONS=--max-old-space-size=8192
```

* Note: Following changes you don't need to do, If these are already deployed (if you are using an existing instance).
* Note: Every time if you are deploying any new changes. You have to restart the appropriate services.

```shell
    sudo systemctl restart server_app_v001_run_app_py.service
    sudo systemctl restart server_app_v001_run_celery.service
    sudo systemctl restart server_app_v001_run_dynamic_scheduler.service
```
#### Step 6: Deploy the application as linux services.
* We are having three linux services to deploy our application.
  * server_app_v001_run_app_py.service
  * server_app_v001_run_celery.service
  * server_app_v001_run_dynamic_scheduler.service

* Deploying app service `server_app_v001_run_app_py.service`.
```shell
[Unit]
Description=KPIT Close Loop Services

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/bin/sh /home/rajivt/code/scenario_simulation/source/server_app_v001/run_app_py.sh
ExecStop=/bin/sh /home/rajivt/code/scenario_simulation/source/server_app_v001/myservices01_clean.sh

[Install]
WantedBy=multi-user.target
```
* Copy the above data to the `/etc/systemd/system/server_app_v001_run_app_py.service` file.
* Run the service using the following command
```shell
    sudo systemctl daemon-reload
    sudo systemctl start server_app_v001_run_app_py.service
```
* You might get error due to file permission used in the service file. Please execute following command
```shell
    chmod 777 /home/rajivt/code/scenario_simulation/source/server_app_v001/run_app_py.sh
    chmod 777 /home/rajivt/code/scenario_simulation/source/server_app_v001/myservices01_clean.sh
```
* Restart the service using the following command.
```shell
    sudo systemctl restart server_app_v001_run_app_py.service
```

* Deploying app service `server_app_v001_run_celery.service`.
```shell
[Unit]
Description=KPIT Close Loop Services

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/bin/sh /home/rajivt/code/scenario_simulation/source/server_app_v001/run_celery.sh
ExecStop=/bin/sh /home/rajivt/code/scenario_simulation/source/server_app_v001/myservices01_clean.sh

[Install]
WantedBy=multi-user.target
```
* Copy the above data to the `/etc/systemd/system/server_app_v001_run_celery.service` file.
* Run the service using the following command
```shell
    sudo systemctl daemon-reload
    sudo systemctl start server_app_v001_run_celery.service
```
* Again, You might get error due to file permission used in the service file. Please execute following command.
```shell
    chmod 777 /home/rajivt/code/scenario_simulation/source/server_app_v001/run_celery.sh
    chmod 777 /home/rajivt/code/scenario_simulation/source/server_app_v001/myservices01_clean.sh
```
* Restart the service using the following command.
```shell
    sudo systemctl restart server_app_v001_run_celery.service
```

* Deploying app service `server_app_v001_run_dynamic_scheduler.service`.
```shell
[Unit]
Description=KPIT Close Loop Services

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/bin/sh /home/rajivt/code/scenario_simulation/source/server_app_v001/run_dynamic_scheduler.sh
ExecStop=/bin/sh /home/rajivt/code/scenario_simulation/source/server_app_v001/myservices01_clean.sh

[Install]
WantedBy=multi-user.target    
```

* Copy the above data to the `/etc/systemd/system/server_app_v001_run_dynamic_scheduler.service` file.
* Run the service using the following command
```shell
    sudo systemctl daemon-reload
    sudo systemctl start server_app_v001_run_dynamic_scheduler.service    
```
* Again, You might get error due to file permission used in the service file. Please execute following command.
```shell
    chmod 777 /home/rajivt/code/scenario_simulation/source/server_app_v001/run_dynamic_scheduler.sh
    chmod 777 /home/rajivt/code/scenario_simulation/source/server_app_v001/myservices01_clean.sh
```
* Restart the service using the following command.
```shell
    sudo systemctl restart server_app_v001_run_dynamic_scheduler.service
```
* Now you have set up & deployed all the services, each service will log the `stdout` & `stderr` in following files.
```shell
    tail -f code/scenario_simulation/source/server_app_v001/app.log # logs web application information.
    tail -f code/scenario_simulation/source/server_app_v001/celery_app.log # logs celery application information.
    tail -f code/scenario_simulation/source/server_app_v001/dynamic_scheduler.log # logs dynamic scheduler process information.
```

* Note: If you want them to run & start the service after booting. Please execute the following command.
```shell
    sudo systemctl enable server_app_v001_run_app_py.service
    sudo systemctl enable server_app_v001_run_celery.service
    sudo systemctl enable server_app_v001_run_dynamic_scheduler.service
```

#### Step 7: Setting up the dynamic scheduler configuration (Terraform configuration).
#### I'll take two region and explain the attributes values to be updated.
* Virginia (us-east-1)
* Oregon (us-west-2)

#### Navigate to `terraform configuration` root directory
```shell
    cd code/scenario_simulation/source/server_app_v001/terraform_configuration/var_files
    ls
    oregon.tfvars.json  virginia.tfvars.json
```
* Configuring the `oregon.tfvars.json`.
```shell
    vi oregon.tfvars.json
```
```json
{
  "parameters": {
    "worker_instance": {
      "instance_type": "t2.xlarge", <mention the instance type of worker instance to be spawned!>
      "key_name": "honda-cclp-us-west-2-oregon-001.pem", <mention the appropriate key pair from the oregon region>
      "security_group": [
        "sg-0d7a7e410c26f83b2" <mention the list of security groups from the oregon region>
      ],
      "subnet_id": "subnet-09775a50980ceaa9d", <mention the subnet-id from the oregon region !Important make sure associated subnet in VPC is peered>
      "instance_count": 7 <mention the no of worker instances to be spawned!>
    },
    "region_name": "us-west-2" <mention the region code (oregon)>
  },
  "ami_copy": {
    "source_ami_id": "ami-0fa1be31209869730", <mention the source ami-id for the worker instance>
    "source_region": "us-east-1" <mention the source region (virginia) inorder to copy the above ami to the destination region (oregon)>
  },
  "s3_bucket": "cclp-migration-data-test-02", <mention the bucket name where the oregon worker instance to read & store input/output data>
  "database_ip": "172.1.0.107" <mention the private-ip of the replicated primary database machine/instance>
}    
```

* Configuring the `virginia.tfvars.json`.
```shell
    vi virginia.tfvars.json
```
```json
{
    "parameters": {
        "worker_instance": {
            "instance_type": "t2.xlarge", <mention the instance type of worker instance to be spawned!>
            "key_name": "honda-cclp-us-east-1-virginia-001", <mention the appropriate key pair from the virginia region>
            "security_group": [
                "sg-0801e05b838796f3b" <mention the list of security groups from the virginia region>
            ],
            "subnet_id": "subnet-0d3f791c0da954c34", <mention the subnet-id from the virginia region !Important make sure associated subnet in VPC is peered>
            "instance_count": 7 <mention the no of worker instances to be spawned!>
        },
        "region_name": "us-east-1" <mention the region code (virginia)>
    },
    "ami_copy": {
        "source_ami_id": "ami-0fa1be31209869730", <mention the source ami-id for the worker instance>
        "source_region": "us-east-1" <mention the source region (virginia) inorder to the copy the above ami to the destination region (virginia)> Note If the source & destination is same, ami wont be copied!
    },
    "s3_bucket": "cclp-migration-data-test-02", <mention the bucket name where the virginia worker instance to read & store input/output data>
    "database_ip": "172.1.0.107" <mention the private-ip of the replicated primary database machine/instance>
}
```
#### Now you have set up the application to use two region i.e (Virginia & Oregon).
## Note: These similar information should be there in config.json. Dynamic scheduler ultimately refer the config.json to spawn the infra & will refer the above tf var files for other information. 
```json
{
  "DYNAMIC_SCHEDULING" : {
    "enabled" : true <enable it to use dynamic scheduler>,
    "tf_directory" : "/home/kpit/code/scenario_simulation/source/server_app_v001/terraform_configuration" ,
    "infra" : { 
      "<region>": {
        "bench_ami": "<mention the bench-ami from the region "region">",
        "subnet_id": "<mention the subnet-id from the region "region">",
        "security_group_id" : "<mention the security group id from the region "region">",
        "initiation_count" : 1,
        "worker_count" : 1, <mention the number of instances to spawned in the region "region">
      },
      "us-east-1" : {
        "bench_ami" : "ami-0c7fe07fc500c52c4", <mention the bench-ami from the region "us-east-1">
        "subnet_id" : "subnet-08b30123", <mention the subnet-id from the region "us-east-1">
        "security_group_id" : "sg-2d263c63", <mention the security group id from the region "us-east-1">
        "initiation_count" : 1,
        "worker_count" : 1, <mention the number of instances to spawned in the region "us-east-1">
        "var_file" : "/home/kpit/code/scenario_simulation/source/server_app_v001/terraform_configuration/var_files/virginia.tfvars.json"
     },
      "us-west-2" : {
        "bench_ami" : "ami-022ff373521efa2a8", <mention the bench-ami from the region "us-west-2">
        "subnet_id" : "subnet-2658874d", <mention the subnet-id from the region "us-west-2">
        "security_group_id" : "sg-d7ad6fa9", <mention the security group id from the region "us-west-2">
        "initiation_count" : 1,
        "worker_count" : 1, 
        "var_file" : "/home/kpit/code/scenario_simulation/source/server_app_v001/dynamic_scheduling/terraform_configuration/var_files/oregon.tfvars.json"
      }
    }
  }
}
```

### Now application is set up & ready to schedule for execution.
#### Speaking of scheduling an execution. There are some checklist to be maintained.
#### Please ensure below checklist is clean before scheduling an execution.

### Checklist 1: Please make sure appropriate SQS Queue doest not contain any messages before starting an execution.
#### Appropriate SQS Queues length should be zero size. It's applicable to all the regions where the infra to be spawned! (Regions configured in Dynamic scheduler.)

### Checklist 2: Please make sure appropriate collection is clean.
#### Drop the following collections 
```shell
    ubuntu@domain:~$ mongosh -u demouser1 -p --authenticationDatabase close_loop_validation
    Enter password: ********
    Current Mongosh Log ID:	628ca04094755031d7361b2c
    Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.3.1
    Using MongoDB:		5.0.6
    Using Mongosh:		1.3.1
    
    For mongosh info see: https://docs.mongodb.com/mongodb-shell/
    
    Warning: Found ~/.mongorc.js, but not ~/.mongoshrc.js. ~/.mongorc.js will not be loaded.
      You may want to copy or rename ~/.mongorc.js to ~/.mongoshrc.js.
    rs0 [direct: primary] test> use close_loop_validation
    switched to db close_loop_validation
    rs0 [direct: primary] close_loop_validation> show collections
    ad_version_management
    analytics_preprocess_collection
    artefact_management
    aws_instance_audit_record
    aws_instance_record
    aws_instance_test_run_status_record
    base_scenario_variation_count_manager
    bench_system_information_record
    deployed_regions # drop these collections before starting an execution
    detailed_kpi_status_record
    docker_info_collection
    kpi_file_extraction_status_record
    kpi_status_record
    master_base_scenario_count_manager
    messages
    messages.broadcast
    messages.routing
    mongoengine.counters
    replicationTest
    report_manager_record
    scenario_drive_session
    scenario_status_information_record
    scenario_status_record
    ticket_id_management
    ticketing_system_record
    tm_report_error_log
    tm_report_execution_analysis
    tm_report_failed_queue_log
    tm_report_failed_scenario
    tm_report_status_test_run_id_topology_mapping
    tm_report_system_performance
    tm_report_total_execution_time
    tm_report_total_execution_time_for_docker
    topology # drop these collections before starting an execution
    rs0 [direct: primary] close_loop_validation> db.topology.drop()
    true  
    rs0 [direct: primary] close_loop_validation> db.deployed_regions.drop()
    true
```
#### Make sure in the mongodb `aws_instance_record` collection, any documents `instance_state` are not in `running` or `pending` state.
#### You can confirm using the following commands.
```shell
    ubuntu@domain:~$ mongosh -u demouser1 -p --authenticationDatabase close_loop_validation
    Enter password: ********
    Current Mongosh Log ID:	628ca04094755031d7361b2c
    Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.3.1
    Using MongoDB:		5.0.6
    Using Mongosh:		1.3.1
    
    For mongosh info see: https://docs.mongodb.com/mongodb-shell/
    
    Warning: Found ~/.mongorc.js, but not ~/.mongoshrc.js. ~/.mongorc.js will not be loaded.
      You may want to copy or rename ~/.mongorc.js to ~/.mongoshrc.js.
    rs0 [direct: primary] test> use close_loop_validation
    switched to db close_loop_validation
    rs0 [direct: primary] close_loop_validation> db.aws_instance_record.distinct('instance_state')
    [ 'shutting-down', 'terminated' ]
```
#### If you see below results, Please execute an update statement to update docs to `terminated` state.
```shell
    rs0 [direct: primary] close_loop_validation> db.aws_instance_record.distinct('instance_state')
    [ 'shutting-down', 'terminated' , 'pending', 'running']
    rs0 [direct: primary] close_loop_validation> db.aws_instance_record.updateMany({instance_state: 'pending'}, {$set: {instance_state: 'terminated'}})
    rs0 [direct: primary] close_loop_validation> db.aws_instance_record.updateMany({instance_state: 'running'}, {$set: {instance_state: 'terminated'}})
    rs0 [direct: primary] close_loop_validation> db.aws_instance_record.distinct('instance_state')
    [ 'shutting-down', 'terminated' ]
```

#### Make sure terraform configuration output is clear, else Please destroy the resources.
* List all the workspaces.
```shell
    $ cd code/scenario_simulation/source/server_app_v001/terraform_configuration
    code/scenario_simulation/source/server_app_v001/terraform_configuration:~$ terraform workspace list
    default
    us-east-1
    us-west-2 * 
```
* Select the specific workspace `us-west-2`
```shell
    code/scenario_simulation/source/server_app_v001/terraform_configuration:~$ terraform workspace select us-west-2
```
* Display the list of resources spawned using terraform. (Everytime it should return below output)
```shell
    code/scenario_simulation/source/server_app_v001/terraform_configuration:~$ terraform output    
    ╷
    │ Warning: No outputs found
    │ 
    │ The state file either has no outputs defined, or all the defined outputs are empty. Please define an output in your configuration with the `output` keyword and run `terraform
    │ refresh` for it to become available. If you are using interpolation, please verify the interpolated value is not empty. You can use the `terraform console` command to assist.
    ╵    
```
* If it gives output like below, Destroy the resources.
```shell
    code/scenario_simulation/source/server_app_v001/terraform_configuration:~$ terraform output
    database_ip: 172.0.1.17
    ami_id: ami-0ac3f6846a418fc75
    worker_ip: [
      10.0.3.14,
      10.0.2.12
    ]
    code/scenario_simulation/source/server_app_v001/terraform_configuration:~$ terraform destroy --var-file="var_files/oregon.tfvars.json" # Please use the respective region var files while destroying.
```

### Now all things are set, You can upload a topology with valid scenario group and an execution can be scheduled.

