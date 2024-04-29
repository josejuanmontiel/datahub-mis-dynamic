import pytest

from unittest.mock import patch

from datahub.ingestion.api.common import PipelineContext

from my_source import custom_ingestion_source as cis

def _base_config():
    return {"env": "file.txt", "rootPath":"tests/unit/single_mce.json"}

class TestCustomIngestionSource:

    def test_initial_database(create_engine_mock):
        config = cis.MyCustomSourceConfig.parse_obj(_base_config())
        source: cis.MyCustomSource = cis.MyCustomSource(config, PipelineContext(run_id="test"))
        for i in source.get_workunits_internal():
            iter = i.get_metadata
            pass
