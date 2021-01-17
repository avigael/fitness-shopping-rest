# REST API Example

This project is written in Python. To run this project please make sure you have [Python](https://www.python.org/downloads/ "Python") installed on your machine.

This REST API is written in Python using Flask and several other libraries. The purpose of this API is to create users, authenticate them with tokens, and store their information as well as contain information on food items and shopping items for two other projects I made. These projects include a [Fitness App](https://github.com/avigael/react-native-fitness-app "Fitness App") using React Native and a [Shopping Website](https://github.com/avigael/dialogflow-shopping-site "Shopping Website") which implements a [DialogFlow](https://dialogflow.cloud.google.com/ "DialogFlow") assistant.

You can read more about how to use the API in the **`/fitness`** and **`/shopping`** directories.

#### Note:

This API is being hosted on a free service provided by Heroku. So it may take a while to start up the server. (Usually 30s - 1min)

## Running Locally
**Download Repository**
```
$ git clone https://github.com/avigael/REST-example.git
$ cd REST-example
```

**Optional:** Create a virtual enviroment

*Note: Only avaliable in [Python 3.3](https://docs.python.org/3/library/venv.html "Python")* and above

```
$ python -m venv venv
$ source venv/bin/activate
```
**Install Requirements:**
```
$ pip install -r requirements.txt
```
**Run the Program**
```
$ python api.py
```