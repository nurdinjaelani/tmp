import flask
import math
import talisker

from canonicalwebteam.discourse_docs import (
    DiscourseAPI,
    DiscourseDocs,
    DocParser,
)

session = talisker.requests.get_session()


def init_tutorials(app, url_prefix):
    discourse_parser = DocParser(
        api=DiscourseAPI(
            session=session, base_url="https://discourse.juju.is/"
        ),
        index_topic_id=2628,
        category_id=34,
        url_prefix=url_prefix,
    )
    discourse_docs = DiscourseDocs(
        parser=discourse_parser,
        document_template="tutorials/tutorial.html",
        url_prefix=url_prefix,
        blueprint_name="tutorials",
    )

    @app.route(url_prefix)
    def index():
        page = flask.request.args.get("page", default=1, type=int)
        posts_per_page = 12
        discourse_docs.parser.parse()
        metadata = discourse_docs.parser.metadata
        total_pages = math.ceil(len(metadata) / posts_per_page)

        return flask.render_template(
            "tutorials/index.html",
            navigation=discourse_docs.parser.navigation,
            forum_url=discourse_docs.parser.api.base_url,
            metadata=metadata,
            page=page,
            posts_per_page=posts_per_page,
            total_pages=total_pages,
            active_section="tutorials",
        )

    discourse_docs.init_app(app)
