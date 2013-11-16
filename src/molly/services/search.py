from pyelasticsearch import ElasticSearch


class Service(ElasticSearch):

    def __init__(self, flask_app):
        super(Service, self).__init__(flask_app.config.get('ELASTICSEARCH_URL', 'http://localhost:9200/'))
