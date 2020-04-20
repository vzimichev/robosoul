from utils import *
        
if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description='String')
    parser.add_argument('--name','-n', type = str, help='Name of launch to use. [default = ""]',default='')
    
    args = parser.parse_args()
    name = args.name
    if name != '': name=f"{name}."
    
    with open("config.json", "r") as config_file: CONFIG = json.load(config_file)
    for i in CONFIG: 
        i.update({'source': f"{name}{'.'.join(i['source'].split('.')[-2:])}"})
        i.update({'supervisor': f"{name}{'.'.join(i['supervisor'].split('.')[-2:])}"})

    with open("config.json", "w") as config_file:
        json.dump(CONFIG,config_file,indent=4)
    output('Session of changer.py ended in ','time',time.time()-start_time) 
