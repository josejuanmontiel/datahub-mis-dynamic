import os
import pytest

from unittest.mock import patch

from datahub.ingestion.api.common import PipelineContext

from my_source import mis_source as cis

def _base_config():
    return [
        {"env": "DEV", "absolute":"false", "rootPath":"../../tests/unit/single_mce.json"},
        {"env": "PRO", "absolute":"true", "rootPath":os.path.dirname(__file__)+"/unit/single_mce.json"},
        {"env": "PRO", "absolute":"true", "rootPath":os.path.dirname(__file__)+"/unit/single_mce_dataset.json"}
    ]

class TestCustomIngestionSource:

    def test_initial_relative(create_engine_mock):
        config = cis.DynamicSourceConfig.parse_obj(_base_config()[0])
        source: cis.DynamicSource = cis.DynamicSource(config, PipelineContext(run_id="test"))
        for i in source.get_workunits_internal():
            iter = i.get_metadata
            pass

    def test_initial_absolute(create_engine_mock):
        config = cis.DynamicSourceConfig.parse_obj(_base_config()[1])
        source: cis.DynamicSource = cis.DynamicSource(config, PipelineContext(run_id="test"))
        for i in source.get_workunits_internal():
            iter = i.get_metadata
            # Assert name inside Owner... is Unit 
            pass

    def test_initial_dataset(create_engine_mock):
        config = cis.DynamicSourceConfig.parse_obj(_base_config()[2])
        source: cis.DynamicSource = cis.DynamicSource(config, PipelineContext(run_id="test"))
        for i in source.get_workunits_internal():
            iter = i.get_metadata
            # Assert name inside Owner... is Unit 
            pass
