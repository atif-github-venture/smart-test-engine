from elasticsearch import Elasticsearch


def connect_elasticsearch(host, port):
    _es = None
    _es = Elasticsearch([{'host': host, 'port': port}])
    if _es.ping():
        print('Yay Connected')
    else:
        print('Awww it could not connect!')
    return _es


class ElasticSearch():
    def create_index(self, es_object, index_name):
        created = False
        settings = {
            'settings': {
                'number_of_shards': 1
            },
            'mappings': {
                '_doc': {
                    'properties': {
                        'Steps': {
                            'properties': {
                                'action': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'data': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'error': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'identifier': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'status': {
                                    'type': 'boolean'
                                }
                            }
                        },
                        'duration': {
                            'type': 'float'
                        },
                        'end_time': {
                            'type': 'date'
                        },
                        'execution_time': {
                            'type': 'date'
                        },
                        'start_time': {
                            'type': 'date'
                        },
                        'status': {
                            'type': 'boolean'
                        },
                        'test_build_info': {
                            'properties': {
                                'additionaltags': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'buildnumber': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'datanamespace': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'filter': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'project': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'runconfiguration': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                },
                                'testtags': {
                                    'type': 'text',
                                    'fields': {
                                        'keyword': {
                                            'type': 'keyword'
                                        }
                                    }
                                }
                            }
                        },
                        'testname': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
                }
            }
        }

        try:
            if not es_object.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                import json
                es_object.indices.create(index=index_name, ignore=400, body=json.dumps(settings))
                print('Created Index for index name -> ' + index_name)
            created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created

    def store_record(self, elastic_object, index_name, record):
        is_stored = True
        try:
            outcome = elastic_object.index(index=index_name, doc_type='_doc', body=record)
            print(outcome)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))
            is_stored = False
        finally:
            return is_stored

    def post_to_elasticsearch(self, host, port, index, content):
        es = connect_elasticsearch(host, port)
        if es is not None:
            if self.create_index(es, index):
                import json
                out = self.store_record(es, index, json.loads(content))
                print('Data indexed successfully!!!') if out else print('Data indexing failed!!!')
