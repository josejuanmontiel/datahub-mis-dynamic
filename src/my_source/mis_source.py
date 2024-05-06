import json
import os

from enum import auto
from typing import Iterable

from datahub.configuration.common import ConfigModel
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.metadata.com.linkedin.pegasus2avro.mxe import MetadataChangeEvent


from pydantic import validator
from pydantic.fields import Field

from datahub.configuration.common import ConfigEnum, ConfigModel, ConfigurationError
from datahub.configuration.validate_field_deprecation import pydantic_field_deprecated

class FileReadMode(ConfigEnum):
    STREAM = auto()
    BATCH = auto()
    AUTO = auto()

class DynamicSourceConfig(ConfigModel):
    env: str = "PROD"
    absolute: bool = False
    rootPath: str = "../example_mce/single_mce.json"

class DynamicSource(Source):
    source_config: DynamicSourceConfig
    report: SourceReport = SourceReport()

    def __init__(self, config: DynamicSourceConfig, ctx: PipelineContext):
        super().__init__(ctx)
        self.source_config = config

    @classmethod
    def create(cls, config_dict, ctx):
        config = DynamicSourceConfig.parse_obj(config_dict)
        return cls(config, ctx)

    def get_workunits_internal(self) -> Iterable[MetadataWorkUnit]:
        relative = ""
        if ~self.source_config.absolute:
            relative = os.path.dirname(__file__)

        with open(
            os.path.join(relative, self.source_config.rootPath),
            "r",
        ) as f:
            obj = json.load(f)
            item = MetadataChangeEvent.from_obj(obj)
            wu = MetadataWorkUnit("single_mce", mce=item)
            self.report.report_workunit(wu)
            yield wu

    def get_report(self) -> SourceReport:
        return self.report

    def close(self) -> None:
        pass

