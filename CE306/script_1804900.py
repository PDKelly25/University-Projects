import json
from elasticsearch import helpers, Elasticsearch #helper functions that abstract some specifics of the raw API - helps with formatting
import re

## Student ID - 1804900

def indexing(): 
    with open('./sample-1M.jsonl', 'r') as json_file: # loading the file (within the same directory as the script)
        
        index_name = 'signal_media_one_million_news_articles' # declaring necessary variables
                                                              # - keeps the schema easily maintainable
        doctype = 'news_articles_index' 
        line = 0 #integer for doc id
        
        es.indices.delete(index=index_name, ignore=[400, 404]) #this is to delete the index as it was created before (testing elasticsearch connection)
        es.indices.create(index=index_name, ignore=400) #create the index again
        es.indices.put_mapping( # mapping indices to data fields (as the dataset is formatted in a specific way)
            index=index_name,doc_type=doctype,
            ignore=400,
            body={ # index body - structure of data fields and the data they contain
                doctype: {
                    "properties": { #structuring the index by each field within the dataset (the article's id, content, title etc.)
                        "id": {
                            "type": "keyword", #declaring each data field's (variable) type - each id is unique but structured similarly, so type keyword is appropriate
                            },
                        "content": {
                            "type": "text", #simply text contained within this data field
                            },
                        "title": {
                            "type": "text",
                            },
                        "media-type": {
                            "type": "keyword", #only 2 values - News and Blog (keyword type meets the requirements)
                            },
                        "source": {
                            "type": "text",
                            },
                        "published": {
                            "type": "date_time_no_millis" # specific format within elastic search that matches the format of the article's published date
                            }
                        }
                    }
                }
            )
        
        
        for json_line in json_file: # for each line within the JSONL file
            line+=1 # necessary for the document id, which is represented by the line number within the dataset file
            json_obj = json.loads(json_line) #create a JSON object from each line within the dataset

            # put document into elastic search            
            es.index(index=index_name, doc_type=doctype, id=line, body=json_obj)
            #print(json_obj)
            print(f"amount of articles uploaded to index: {line}") # ouput to python shell the amount of articles that have been indexed (keeping track)
          

    json_file.close()

def test_collection(): # contains main query for test collection, as well as other typical user queries
    body = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "protest"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }

    result1 = es.search(index="signal_media_one_million_news_articles", body=body)
    #print(result1)
    

    query_article1 = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "marathon protest",  
                                      "operator": "and"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }

    result2 = es.search(index="signal_media_one_million_news_articles", body=query_article1)
    #print(result2)

    query2_article1 = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "twin cities marathon"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "protest"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }

    result3 = es.search(index="signal_media_one_million_news_articles", body=query2_article1)
    #print(result3)

    query_article2 = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "query_string": {
                                  "query": "(protest*) AND (start*)"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "minnesota"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }

    result4 = es.search(index="signal_media_one_million_news_articles", body=query_article2)
    #print(result4)

    query2_article2 = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "hate group"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "query_string": {
                                  "query": "Eli*abeth Hasselback" # Elisabeth or Elizabeth"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "protest movement",
                                      "operator": "and"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }
        
    result5 = es.search(index="signal_media_one_million_news_articles", body=query2_article2)
    #print(result5)

    query_article3 = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "Baltimore police officers"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "query_string": {
                                  "query": "Fred* Gray" # Fred, Freddie, Freddy
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "protest charged death",
                                      "operator": "and"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }

    result6 = es.search(index="signal_media_one_million_news_articles", body=query_article3)
    #print(result6)

    query2_article3 = {
        "query": {
            "bool": {
                "must": [
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "black lives matter"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "Baltimore Mayor Stephanie Rawlings-Blake"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "Interim Police Commissioner Kevin Davis"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match_phrase": {
                                  "content": "press conference"
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "query_string": {
                                  "query": "officer*" # Officer, officers
                                  }
                              }]
                          }
                      },
                  {
                      "bool": {
                          "must": [{
                              "match": { 
                                  "content": {
                                      "query": "protest trial police",
                                      "operator": "and"
                                      }
                                  }
                              }]
                          }
                      }
                  ],
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }

    result7 = es.search(index="signal_media_one_million_news_articles", body=query2_article3)
    #print(result7)

    return (body, query_article1, query2_article1, query_article2, query2_article2, query_article3, query2_article3)

def update_settings(): #elasticsearch indices cannot be open when updating index settings

    tfidf_mapping = { # index body - structure of data fields and the data they contain
        "properties": { #structuring the index by each field within the dataset (the article's id, content, title etc.)
            "id": {
                "type": "keyword", #declaring each data field's (variable) type - each id is unique but structured similarly, so type keyword is appropriate
                },
            "content": {
                "type": "text", #simply text contained within this data field
                "similarity": "BM25"
                },
            "title": {
                "type": "text",
                "similarity": "BM25"
                },
            "media-type": {
                "type": "keyword", #only 2 values - News and Blog (keyword type meets the requirements)
                },
            "source": {
                "type": "text",
                },
            "published": {
                "type": "date_time_no_millis" # specific format within elastic search that matches the format of the article's published date
                }
            }
        }

    boolean_mapping = { # index body - structure of data fields and the data they contain
        "properties": { #structuring the index by each field within the dataset (the article's id, content, title etc.)
            "id": {
                "type": "keyword", #declaring each data field's (variable) type - each id is unique but structured similarly, so type keyword is appropriate
                },
            "content": {
                "type": "text", #simply text contained within this data field
                "similarity": "boolean"
                },
            "title": {
                "type": "text",
                "similarity": "boolean"
                },
            "media-type": {
                "type": "keyword", #only 2 values - News and Blog (keyword type meets the requirements)
                },
            "source": {
                "type": "text",
                },
            "published": {
                "type": "date_time_no_millis" # specific format within elastic search that matches the format of the article's published date
                }
            }
        }

    tfidf_settings = { # MAY HAVE TO CHANGE TO MAPPING - would be viable if index was dynamic, but it is static - settings cannot be changed
        "settings": {
            "index": {
                "similarity": {
                    "type": "BM25"
                    }
                }
            }
        }

    boolean_settings = {
            "settings": {
                "index": {
                    "similarity": {
                        "type": "boolean"
                        }
                    }
                }
            }
    
    #es.indices.put_settings(body=boolean_settings)
    #es.indices.put_settings(body=tfidf_settings)

    es.indices.put_mapping(index="signal_media_one_million_news_articles", ignore=400, body=tfidf_mapping)
    #es.indices.put_mapping(index="signal_media_one_million_news_articles", ignore=400, body=boolean_mapping)

def evaluate(testcollection, query_article1, query2_article1, query_article2, query2_article2, query_article3, query2_article3):

    ## boolean version of test collection query

    boolean_ver_testcollect = {
        "query": {
            "bool": {
                "must":
                {
                    "match": {
                        "content": {
                            "query": "black lives matter protest",
                            "operator": "and"
                            }
                        }
                    },
                "filter":{
                    "term": {
                        "media-type.keyword": "News"
                        }
                    }
                }
            },
        "sort": {
            "_score": "desc"
            }
        }
    
    result = es.search(index="signal_media_one_million_news_articles", body=boolean_ver_testcollect)
    #print(result)
    
    ##

    boolean_query_testcollect = {
        "requests": [
            {
                "id": "query_article1", #the id of this request
                "request": boolean_ver_testcollect, # variable name of query being evaluated
                "ratings": [ # ratings of relevance based on information need
                    {
                        "_id": "38146",
                        "rating": "3", #0 - not relevant at all, 1 - a little relevant, 2 - relevant, 3 - very relevant (the most relevant)
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "31013",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "53148",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "57460",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "51274",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "41734",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "53444",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "32108",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "34375",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "7500",
                        "rating": "0",
                        "_index": "signal_media_one_million_news_articles"
                        }
                    ]
                } ],
        "metric": { 
            "precision": { # P @ K metric
                "k": 5, # top 5 relevant documents
                "relevant_rating_threshold": 2 # anything rated 2 or more is relevant, anything else is irrelevant, or not relevant enough
                }
            }
        }

    query_testcollect = {
        "requests": [
            {
                "id": "query_article1",
                "request": testcollection,
                "ratings": [
                    {
                        "_id": "51274",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "31013",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "53148",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "38146",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "57460",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "41734",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "53444",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "32108",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "34375",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }
    
    query1 = {
        "requests": [
            {
                "id": "query_article1",
                "request": query_article1,
                "ratings": [
                    {
                        "_id": "51274",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "32108",
                        "rating": "1",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "34375",
                        "rating": "1",
                        "_index": "signal_media_one_million_news_articles"
                        }
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }

    query2 = {
        "requests": [
            {
                "id": "query_article1",
                "request": query2_article1,
                "ratings": [
                    {
                        "_id": "51274",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        }
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }

    query3 = {
        "requests": [
            {
                "id": "query_article1",
                "request": query_article2,
                "ratings": [
                    {
                        "_id": "31013",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "53148",
                        "rating": "2",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "587",
                        "rating": "1",
                        "_index": "signal_media_one_million_news_articles"
                        }
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }

    query4 = {
        "requests": [
            {
                "id": "query_article1",
                "request": query2_article2,
                "ratings": [
                    {
                        "_id": "31013",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "53148",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles",
                        }
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }

    query5 = {
        "requests": [
            {
                "id": "query_article1",
                "request": query_article3,
                "ratings": [
                    {
                        "_id": "32108",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "34375",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }

    query6 = {
        "requests": [
            {
                "id": "query_article1",
                "request": query2_article3,
                "ratings": [
                    {
                        "_id": "32108",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    {
                        "_id": "34375",
                        "rating": "3",
                        "_index": "signal_media_one_million_news_articles"
                        },
                    ]
                } ],
        "metric": {
            "precision": {
                "k": 5,
                "relevant_rating_threshold": 2
                }
            }
        }
    
    result_eval1 = es.rank_eval(boolean_query_testcollect, index="signal_media_one_million_news_articles")
    result_eval2 = es.rank_eval(query_testcollect, index="signal_media_one_million_news_articles")
    result_eval3 = es.rank_eval(query1, index="signal_media_one_million_news_articles")
    result_eval4 = es.rank_eval(query2, index="signal_media_one_million_news_articles")
    result_eval5 = es.rank_eval(query3, index="signal_media_one_million_news_articles")
    result_eval6 = es.rank_eval(query4, index="signal_media_one_million_news_articles")
    result_eval7 = es.rank_eval(query5, index="signal_media_one_million_news_articles")
    result_eval8 = es.rank_eval(query6, index="signal_media_one_million_news_articles")
    #print(result_eval1)
    #print(result_eval2)
    #print(result_eval3)
    #print(result_eval4)
    #print(result_eval5)
    #print(result_eval6)
    #print(result_eval7)
    print(result_eval8)

        
try:
    # make connection to elasticsearch server (localhost:9200)
    es = Elasticsearch("http://localhost:9200")
    es = Elasticsearch()

except Exception as error:
    print ("Elasticsearch client ERROR:", error)
    es = None


# index Signal Media One Million News Article dataset
if not es.indices.exists(index="signal_media_one_million_news_articles"): #check if index is already created as otherwise the documents would be uploaded for each run of the script
    indexing()

# perform elasticsearch queries for test collection to search user queries
test = test_collection()

#method to update index settings for evaluation
update_settings()

# evaluation method
evaluate(test[0], test[1], test[2], test[3], test[4], test[5], test[6])
