import gzip

import tornado.escape
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
        self.event_service = self.application.event_service
        self.set_header("Content-Type", "application/json")


class StoreHandler(BaseHandler):
    async def post(self, project_id: int):
        encode = self.request.headers.get("Content-Encoding")
        body = self.request.body
        if encode == "gzip":
            body = tornado.escape.json_decode(gzip.decompress(body))

        event = self.event_service.event_from_json(body, project_id)
        response = {"id": event.id}
        self.write(tornado.escape.json_encode(response))
