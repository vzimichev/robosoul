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
        src = f"{name}{'.'.join(i['source'].split('.')[-2:])}"
        svr = f"{name}{'.'.join(i['supervisor'].split('.')[-2:])}"
        try:
            with open(src, "r") as file: pass
            with open(svr, "r") as file: pass
        except:
            output('File exception occured.','error')
            output(f"Problem with: {name}")
            break
        i.update({'source': src})
        i.update({'supervisor': svr})

    with open("config.json", "w") as config_file:
        json.dump(CONFIG,config_file,indent=4)
    output('Session of changer.py ended in ','time',time.time()-start_time) 
