from PipelineRun import PipelineRun
from TriggerSchedule import TriggerSchedule
from Sinks.SinkConnector import SinkConnector
from Embeds.EmbedConnector import EmbedConnector
from Sources.SourceConnector import SourceConnector
from Embeds import as_embed
from Sinks import as_sink

from typing import List, Tuple

accepted_trigger_sync_types: List = []
class Pipeline(object):
    def __init__(self, 
                source:  List[SourceConnector], # Change to only support a list of Sources for V2
                embed: EmbedConnector, 
                sink: SinkConnector, 
                name:str = None,
                id: str = None, 
                version: str = "v2",
                created: float = None, 
                updated: float = None,
                trigger_schedule: TriggerSchedule = None, 
                latest_run: PipelineRun = None, 
                owner: str = None, 
                is_deleted: bool = False):
        self.id = id
        self.name = name
        self.version = version
        self.created = created
        self.updated = updated
        self.source = source
        self.embed = embed
        self.sink = sink
        self.trigger_schedule = trigger_schedule
        self.latest_run = latest_run 
        self.owner = owner
        self.is_deleted = is_deleted

    def validate(self) -> bool:
        """Running validation for each connector"""
        try:
            for source in self.source:
                source.validation()
            self.embed.validation()
            # Missing sink validation
        except Exception as e:
            raise e
                 
    def toPipelineModel(self):
        content_to_return = {}
        content_to_return['id'] = self.id
        content_to_return['name'] = self.name
        content_to_return['version'] = "v2"
        content = []
        for source in self.source:
            content.append(source.to_model())
        content_to_return['source'] = content
        content_to_return['embed'] = self.embed.to_model()
        content_to_return['sink'] = self.sink.to_model()
        content_to_return['created'] = self.created
        content_to_return['updated'] = self.updated
        if self.trigger_schedule == None:
            content_to_return['trigger_schedule'] = None
        else:
            content_to_return['trigger_schedule'] = self.trigger_schedule.to_model()

        content_to_return['latest_run'] = self.latest_run.toJson()

        return content_to_return
    def toJson(self):
        """Python does not have built in serialization. We need this logic to be able to respond in our API..

        Returns:
            _type_: the json to return
        """
        json_to_return = {}
        json_to_return['id'] = self.id
        json_to_return['name'] = self.name
        json_to_return['version'] = "v2"
        json_source = []
        for source in self.source:
            json_source.append(source.toJson())
        json_to_return['source'] = json_source
        json_to_return['embed'] = self.embed.toJson()
        json_to_return['sink'] = self.sink.toJson()
        json_to_return['owner'] = self.owner
        json_to_return['created'] = self.created
        json_to_return['updated'] = self.updated
        json_to_return['is_deleted'] = self.is_deleted

        if self.trigger_schedule == None:
            json_to_return['trigger_schedule'] = None
        else:
            json_to_return['trigger_schedule'] = self.trigger_schedule.toJson()

        json_to_return['latest_run'] = self.latest_run.toJson()
        return json_to_return

    def as_request(self):
        json_body = {}
        json_source = []
        for source in self.source:
            json_source.append(source.toJson())
        json_body['source'] = json_source
        json_body['embed'] = self.embed.toJson()
        json_body['sink'] = self.sink.toJson()
        return json_body

    def set_id(self, id: str):
        self.id = id
    
    def set_created(self, created: float):
        self.created = created

    def set_updated(self, updated: float):
        self.updated = updated

    def set_latest_run(self, pipeline_run: PipelineRun):
        self.latest_run = pipeline_run

    def set_owner(self, owner: str):
        self.owner = owner
    
    def as_pipeline(dct:dict):
        if dct == None:
            return None
        
        source = dct.get("source")
        source_value = []
        for s in source:
            source_value.append(SourceConnector.as_source_connector(s))
        return Pipeline(
            name=dct.get("name", None),
            id=dct.get("id", None),
            source=source_value,
            embed = as_embed(dct.get("embed")),
            sink = as_sink(dct.get("sink")),
            trigger_schedule=TriggerSchedule.as_trigger_schedule(dct.get("trigger_schedule", None)),
            latest_run=PipelineRun.as_pipeline_run(dct.get("latest_run", None)),
            created=dct.get("created", None),
            updated=dct.get("updated", None),
            owner=dct.get("owner", None),
            is_deleted=dct.get("is_deleted", False)
        )