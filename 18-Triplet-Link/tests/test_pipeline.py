import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import os
from src.pipeline.step0_preprocess import Step0Preprocessor
from src.pipeline.step2_candidates import Step2CandidateGenerator
from src.pipeline.step3_relations import Step3RelationMapper
from src.pipeline.step4_disambiguation import Step4Aligner
from src.pipeline.step5_facts import Step5FactGenerator
from src.pipeline.step6_graph import Step6GraphBuilder
from src.config import config

class TestPipeline(unittest.TestCase):
    
    def setUp(self):
        # Setup temporary paths or mocks if possible
        # For simplicity, we mock pandas read_csv/to_csv or the data itself
        pass

    @patch('src.pipeline.step0_preprocess.pd.read_csv')
    @patch('src.pipeline.step0_preprocess.pd.DataFrame.to_csv')
    def test_step0(self, mock_to_csv, mock_read_csv):
        # Mock inputs
        mock_read_csv.side_effect = [
            pd.DataFrame({
                'Row_Index': ['A_1'],
                'Index': [1],
                '主体 (Subject)': ['S'],
                '谓词 (Predicate)': ['P'],
                '客体 (Object)': ['O']
            }),
            pd.DataFrame({
                'index': ['A_1'],
                'Index_Main Entry': ['Entry']
            })
        ]
        
        Step0Preprocessor().run()
        mock_to_csv.assert_called()

    @patch('src.services.wikidata.wikidata_service.search_entity')
    @patch('src.pipeline.step2_candidates.pd.read_csv')
    @patch('src.pipeline.step2_candidates.pd.DataFrame.to_csv')
    def test_step2(self, mock_to_csv, mock_read_csv, mock_search):
        mock_read_csv.return_value = pd.DataFrame({
            'triple_id': ['T1'],
            'subject': ['S'],
            'object': ['O']
        })
        mock_search.return_value = [{'id': 'Q1', 'label': 'S', 'description': 'desc', 'url': ''}]
        
        Step2CandidateGenerator().run()
        mock_to_csv.assert_called()

    @patch('src.pipeline.step3_relations.pd.read_csv')
    @patch('src.pipeline.step3_relations.pd.DataFrame.to_csv')
    def test_step3(self, mock_to_csv, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            'triple_id': ['T1'],
            'relation': ['is_located_in'],
            'subject': ['S'],
            'object': ['O'],
            'source_sentence': 'ctx'
        })
        
        Step3RelationMapper().run()
        mock_to_csv.assert_called()

if __name__ == '__main__':
    unittest.main()
