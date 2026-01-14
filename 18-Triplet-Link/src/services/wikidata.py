import atexit
import requests
import time
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import config

class WikidataService:
    def __init__(self):
        self.cache_file = config.DATA_DIR / "wikidata_cache.json"
        self.cache = self._load_cache()
        self.last_request_time = 0
        self.request_interval = 0.05  # 20 requests per second = 0.05s interval
        atexit.register(self.save)
        
    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_cache(self):
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
            
    def _rate_limit(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.request_interval:
            time.sleep(self.request_interval - elapsed)
        self.last_request_time = time.time()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def search_entity(self, query: str, limit: int = 5, language: str = 'en') -> List[Dict]:
        if not query:
            return []
            
        cache_key = f"search_{query}_{language}_{limit}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        self._rate_limit()
        
        params = {
            'action': 'wbsearchentities',
            'search': query,
            'language': language,
            'limit': limit,
            'format': 'json',
            'type': 'item'
        }
        
        try:
            response = requests.get(
                config.WIKIDATA_API_URL, 
                params=params, 
                headers={'User-Agent': config.USER_AGENT},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get('search', []):
                results.append({
                    'id': item.get('id'),
                    'label': item.get('label'),
                    'description': item.get('description', ''),
                    'url': item.get('url'),
                    # Simple score simulation based on rank/match
                    # In real API, match info might be used
                    'score': 0.0 # Placeholder, will be calculated later or just use rank
                })
            
            # Save to cache
            self.cache[cache_key] = results
            # Periodically save cache to disk (optimization: do it less frequently or on exit)
            if len(self.cache) % 10 == 0:
                self._save_cache()
                
            return results
            
        except Exception as e:
            print(f"Error searching Wikidata for '{query}': {e}")
            raise

    def save(self):
        self._save_cache()

wikidata_service = WikidataService()
