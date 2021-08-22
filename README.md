# Hamato-Yoshi
Hamato-Yoshi is a malware detection system for linux. <br/>
It runs as a [daemon](https://en.wikipedia.org/wiki/Daemon_(computing)#:~:text=In%20multitasking%20computer%20operating%20systems,control%20of%20an%20interactive%20user.&text=In%20a%20Unix%20environment%2C%20the,not%20always%2C%20the%20init%20process.) process and monitors [```/proc```](https://www.kernel.org/doc/Documentation/filesystems/proc.txt) 
for suspicious activity. 

![Hamato Yoshi](docs/img/YoshiTMNTcomic.jpg)<br/>

## Installation
Clone the repository from [Bitbucket](http://mrs-magenta:7990/scm/turtles/hamato-yoshi.git):
```bash
$ git clone http://mrs-magenta:7990/scm/turtles/hamato-yoshi.git
```

Create a local [virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/#:~:text=A%20virtual%20environment%20is%20a,of%20the%20Python%20developers%20use.):
```bash
$ virtualenv -p /usr/bin/python3 venv
```

Activate the virtual environment with:
```bash
$ source venv/bin/activate
(venv)$
```

Install ```requirements.txt``` using pip:
```bash
(venv)$ pip install -r requirements.txt
```

## Usage
```bash
(venv)$ python main.py
```

## Structure
* Hamato-Yoshi continuously takes [snapshots](/snapshot.py) of files in ```/proc/*``` and analyzes their <b>changes</b>.<br/> 
* When it detects a snapshot has <b>changed</b>, Hamato-Yoshi follows a set of  [rules](/rules.py) defined in [rules.csv](/rules.csv) and [proc_rules](/proc_rules.csv). <br/> 
* Each rule defines [actions](/actions.py) to perform if the <b>detected changes</b> meet certain [conditions](/conditions/conditions.py).<br/>
* In order to analyze these <b>changes</b>, Hamato-Yoshi is equipped with tailor-made [parsers](/parsers/__init__.py) for each of the <i>(currently partial list of)</i> files in ```/proc/*```. 
* These parsers yield a comparable structured data (usually a ```dict```) from the contents of the file they parse.   