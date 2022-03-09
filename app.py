
import logging
from urllib import response
from flask import Flask, Response,jsonify,request
import configparser
import boto3
import logging

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("env/config.ini")

client = boto3.client('ec2',
    aws_access_key_id=config["AWS"]["aws_access_key_id"],
    aws_secret_access_key=config["AWS"]["aws_secret_access_key"],
    region_name=config["AWS"]["region_name"]
    )

@app.route("/ec2/list",methods=["Get"])
def ec2InstansList():
    aws_access_key_id = request.args.get("access_key")
    aws_secret_access_key =request.args.get("secret_key")
    region_name = request.args.get("region_name")

    try:
        return getInstanceList()
    except Exception as error:
        return jsonify({'errorStop' : error})

InstanceIds = []
def getInstanceList():
    response = client.describe_instances(    
    )
    
    for instance in response["Reservations"]:
        for i in instance["Instances"]:
            InstanceIds.append(i["InstanceId"])  
    try:
        return jsonify(response)
    except Exception as error:
        return jsonify({'errorStop' : error})

@app.route("/ec2/start",methods=["Get"])
def startInstances():
    aws_access_key_id = request.args.get("access_key")
    aws_secret_access_key =request.args.get("secret_key")
    region_name = request.args.get("region_name")
    InstanceID = request.args.get("InstanceID")
    response = client.start_instances(
        InstanceIds=InstanceIds
    )
    try:
        return response
    except Exception as error:
        return jsonify({'errorStart' : error})

@app.route("/ec2/start/all",methods=["Get"])
def startInstancesAll():
    aws_access_key_id = request.args.get("access_key")
    aws_secret_access_key =request.args.get("secret_key")
    region_name = request.args.get("region_name")
    response = client.start_instances(
        InstanceIds=InstanceIds
    )
    try:
        return response
    except Exception as error:
        return jsonify({'errorStartAll' : error})

@app.route("/ec2/stop",methods=["Get"])
def stopInstances():
    aws_access_key_id = request.args.get("access_key",config["AWS"]["aws_access_key_id"])
    aws_secret_access_key =request.args.get("secret_key",config["AWS"]["aws_secret_access_key"])
    region_name = request.args.get("region_name",config["AWS"]["region_name"])
    InstanceID = request.args.get("InstanceID")
    response = client.stop_instances(
        InstanceIds=InstanceIds
    )
    try:
        return response
    except Exception as error:
        return jsonify({'errorStop' : error})




def getHostInfo(info):    
    Info = config["HostHeader"][info]
    try:
        return Info
    except Exception as error:
        return jsonify({'errorHost' : error})

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
 
@app.route('/ec2/blogs')
def blogLogs():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return f"Welcome to the Blog"

if __name__ == "__main__":
    hostInfo= getHostInfo("host")
    portInfo = getHostInfo("port")

    
    app.run(host="{}".format(hostInfo),port="{}".format(portInfo),debug= True)



#Status code için make_response kullanılacak!