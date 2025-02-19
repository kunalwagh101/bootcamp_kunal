**No.5 :- Now, extend the library to use config.yaml file in the following way: Extend the say_hello function to load a _config.yaml file to get a parameter called "num_times". You repeat the hello that many times and return the result string. Code it such a way that the code looks for the yaml file in the current folder, followed by ':' separated CONFIG_PATH env variable. If none found, it should use a default yaml file that is shipped along with the module. Now encapsulate all the config loading in your code into a different file. Use it in your say_hello file. Package and publish it. Test it with many-hellos cli by, placing a config file in the current working directory. Test another with ATK_CONFIG_PATH variable. Finally, test it without any config file to load from default file.**

**No.6 :-  Add logging to your library (both the files -- sayhello and config reader), using logging library.**


**No.7 :- Turn on the logging when you are executing many-hellos.**


**No.8 :- Turn it off and see.**


**No.9 :- Turn on selectively only for the config reader code and show it works.**

 
***Working localy***

```
python -m many_hellos.main hello kunal

```
or try 

```
python -m many_hellos.main kunal

```
***Install the dependence***

```
pip install --index-url https://test.pypi.org/simple/ many-hellos

``` 


```
python -m many_hellos.main kunal

```

or try 

```
python -m many_hellos.main hello kunal

```

***To access the logs : Run the application with the verbose flag , it turns logs on***

```
python -m many_hellos.main --verbose hello Alice Bob

```


***Enable Only Config Loader Logging***

```
python -m many_hellos.main hello --config-logging Alice 
```