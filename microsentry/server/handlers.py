import gzip

import tornado.escape
import tornado.web

from microsentry import models


class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
        self.set_header("Content-Type", "application/json")


class StoreHandler(BaseHandler):
    async def post(self, project_id: int):
        encode = self.request.headers.get("Content-Encoding")
        body = self.request.body
        if encode == "gzip":
            body = tornado.escape.json_decode(gzip.decompress(body))

        context_obj = body.pop("contexts", {})
        context = models.Context(**context_obj.get("runtime", {}))
        print(context)
        exception_list = []
        for exception_obj in body.pop("exception", {}).get("values", []):
            frame_list = []
            for frame_obj in exception_obj.get("stacktrace", {}).get(
                "frames", []
            ):
                frame_obj.pop("in_app")
                variable_map = frame_obj.pop("vars")
                frame = models.Frame(
                    **{"variable_map": variable_map, **frame_obj}
                )
                print(frame)
                frame_list.append(frame)

            exception = models.SentryException(
                frame_list=frame_list,
                handled=exception_obj.get("mechanism", {}).get("handled"),
                module=exception_obj.get("module"),
                type=exception_obj.get("type"),
                value=exception_obj.get("value"),
            )
            print(exception)
            exception_list.append(exception)

        event_id = body.pop("event_id")
        body.pop("breadcrumbs")
        body.pop("extra")
        body.pop("sdk")
        body.pop("platform")
        body.pop("_meta")
        event = models.Event(
            **{
                "context": context,
                "exception_list": exception_list,
                "project_id": project_id,
                "id": event_id,
                **body,
            }
        )
        print(event)
        response = {"id": event.id}
        self.write(tornado.escape.json_encode(response))
