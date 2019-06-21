# expert-waffleg

## Instructions to reproduce the result

## Requirements - Python3
 
  If you have Python2, Python3 both installed and you use Python2 by default, you may want to execute the code using Python3
  ***
  Python2 users, Python3 installed on the system
    eg:- python3 crawler.py -h
  ***
  Python3 users:
    You can execute normally eg:- python crawler.py
  ***
## Dependencies

* pip install validator_collection
* pip install bs4 
* pip install lxml

- python2 users may want to use pip3
## Execution

1. `python crawler.py -h`
   - would print the usage and give you list of options to be specified as an argument
   
   ```
      Nithins-MacBook-Pro:crawl Nithin$ python crawler.py -h
      usage: crawler.py [-h] [-u URL [URL ...]] [-d DEPTH] [-f]

      optional arguments:
      -h, --help             show this help message and exit
      -u URL [URL ...], --url URL [URL ...]
                             specify the url of the website/s to crawl eg:-
                             https://github.com
      -d DEPTH, --depth DEPTH maximum depth to crawl
                        
      -f, --file            Save output to file
      ```

2. Execute this command to crawl 'github.com' and store the crawled results in the file
- `python crawler.py -u https://github.com -d 2 -f`
- ```
    Nithins-MacBook-Pro:crawl Nithin$ python crawler.py -u https://github.com -d 2 -f
    url ['https://github.com'] depth 2 file True
    Crawl done. Look for the output file at  /Users/Nithin/Desktop/crawl/github.txt
    ```

### Optional arguments
- `-u`  Can input one or more urls. All the parent domain crawls will be saved in domain specific filename
- `-f`  Can leave this blank and results will be printed to console.
