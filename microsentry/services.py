from microsentry import models


class EventService:
    @classmethod
    def event_from_json(cls, data, project_id):
        context_obj = data.pop("contexts", {})
        context = models.Context(**context_obj.get("runtime", {}))
        exception_list = []
        for exception_obj in data.pop("exception", {}).get("values", []):
            frame_list = []
            for frame_obj in exception_obj.get("stacktrace", {}).get(
                "frames", []
            ):
                frame_obj.pop("in_app")
                variable_map = frame_obj.pop("vars")
                frame = models.Frame(
                    **{"variable_map": variable_map, **frame_obj}
                )
                frame_list.append(frame)

            exception = models.SentryException(
                frame_list=frame_list,
                handled=exception_obj.get("mechanism", {}).get("handled"),
                module=exception_obj.get("module"),
                type=exception_obj.get("type"),
                value=exception_obj.get("value"),
            )
            exception_list.append(exception)

        event_id = data.pop("event_id")
        data.pop("breadcrumbs")
        data.pop("extra")
        data.pop("sdk")
        data.pop("platform")
        data.pop("_meta")
        event = models.Event(
            **{
                "context": context,
                "exception_list": exception_list,
                "project_id": project_id,
                "id": event_id,
                **data,
            }
        )
        return event
