from logging import error
from typing import Tuple
import yaml, jsonschema;
import subprocess, sys, os, re;
import command as Command;

class DCTM:
    def __init__(self):
        self.values = {}
    
    def switch(self, template_file, target_path = os.getcwd()+"/docker-compose.yaml", template_values_dict={}):
        self.values = self.__prepare_values(template_values_dict)
        self.__replace_values(template_file, target_path)
        self.validate(target_path)
    
    def __prepare_values(self, template_values_dict):
        """prepare values for overriding file, by running commands and returning string

        Args:
            template_values_dict (dict): dictionary of values that must be overriden

        Returns:
            dict: ready values, with command outputs overwriten
        """
        values = {}
        for i in template_values_dict:
            # Run command and store output
            if "command" in template_values_dict[i]["type"].lower():
                template_values_dict[i]["value"] = self.__command(template_values_dict[i]["value"])
            
            # Parse what type of data it is
            values[i.lower()] = self.__format_value_type(template_values_dict[i])

                
        return values
    
    def __format_value_type(self, value):
        """Redirect data to correct format

        Args:
            value (dict): dictionary of value, including type, value and rtype in case of command

        Returns:
            int, float, string: returns value in correct format
        """
        value_type = value["type"].lower()
        
        try:
            value_type = value["rtype"].lower()
        except Exception as e:
            pass

        # Number
        if "number" in value_type:
            return int(value["value"])
        elif "float" in value_type:
            return float(value["value"])
        # String
        # return '"'+value["value"].replace('"','\"')+'"'
        return value["value"]
    
    def __replace_values(self, template_file, target_path):
        template = open(template_file, "r")
        target = open(target_path, "w")
        
        for line in template:
            if "${{" in line and "}}$" in line:
                pattern = r'\${{(.*?)\}}'
                words = re.findall(pattern, line)
                for word in words:
                    line = line.replace('${{'+word+'}}$', self.values[word])
                target.write(line)
                continue
            target.write(line)
                
        template.close()
        target.close()
                
    
    def __command(self, command):
        """execute command and return output

        Args:
            command (str): command that should be executed

        Returns:
            string: response of command
        """
        try:
            response = subprocess.run(command.split(), stdout=subprocess.PIPE)
            return response.stdout.decode('utf-8').strip()
        except Exception as e:
            error(f"⛔️ Failed command: {command} \n{e}")
            return "ERROR"
    
    def validate(self, compose_file):
        """Validate docker compose file

        Args:
            compose_file (str): path to docker compose file

        Returns:
            bool: return compose file validation result
        """
        try:
            Command.run(["docker", "compose", "-f", compose_file, "config"])
            print(f"{compose_file} - ✅ valid docker compose file")
            return True
        except Exception as e:
            print(f"{compose_file} - ⛔️ invalid docker compose file")
            return False
        
    




def main():
    dctm = DCTM()
        
    dctm.switch(
        "../example/basic/templates.docker/main.dockertemplate.yaml",
        "../docker-compose.test.yaml", 
        {
            "hello": {
                "type": "string",
                "value": 'Hello'
            },
            "goodbye": {
                "type": "command",
                "rtype": "string",
                "value": 'uname -a'
            },
            "environment": {
                "type": "string",
                "value": 'sbx'
            },
            "localport": {
                "type": "int",
                "value": '9200'
            },
            "something": {
                "type": "float",
                "value": '10.21'
            }
        }
    )
    

main()