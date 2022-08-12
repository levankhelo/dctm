"""Handle arguments and run DCTM
"""

from .dctm import DCTM


def main():
    """Basic main function that will be executed
    """
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
